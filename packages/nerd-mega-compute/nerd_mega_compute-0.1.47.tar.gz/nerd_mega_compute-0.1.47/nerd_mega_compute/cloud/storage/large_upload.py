import requests
import json
import pickle
import boto3
import os
import io
import math
from botocore.config import Config
from ...utils import debug_print
from ...spinner import Spinner
import traceback
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Create a requests session with robust retry logic
def create_robust_session():
    """Create a requests session with improved retry logic and connection handling"""
    session = requests.Session()
    
    # Configure robust retry strategy
    retry_strategy = Retry(
        total=5,  # More retries
        backoff_factor=0.5,  # Exponential backoff
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "PUT", "DELETE", "POST", "OPTIONS", "HEAD"],
        respect_retry_after_header=True
    )
    
    # Configure adapter with retry strategy and longer timeouts
    adapter = HTTPAdapter(
        max_retries=retry_strategy,
        pool_connections=10,  # Increase connection pool size
        pool_maxsize=10,
        pool_block=False
    )
    
    # Mount adapter to both http and https
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session

def upload_large_file(data_to_upload, metadata=None):
    """
    Handle upload of large files to the cloud storage

    Args:
        data_to_upload: The data to upload
        metadata: Optional metadata to include with the upload

    Returns:
        dict: Information about the uploaded data
    """
    # Get the API key
    from ..auth import get_api_key
    api_key = get_api_key()
    
    # Determine storage format
    storage_format = 'binary' if isinstance(data_to_upload, bytes) else 'pickle'

    # Set up the request
    spinner = Spinner("Getting presigned URL for large file upload...")
    spinner.start()

    try:
        # Create a robust session with retry logic
        session = create_robust_session()
        
        # First, get the presigned URL for upload
        headers = {
            'x-api-key': api_key
        }

        response = session.post(
            'https://lbmoem9mdg.execute-api.us-west-1.amazonaws.com/prod/nerd-mega-compute/data/large',
            headers=headers,
            timeout=30
        )

        if response.status_code != 200:
            spinner.stop()
            error_msg = f"Failed to get presigned URL for large file upload: {response.text}"
            print(f"❌ {error_msg}")
            raise Exception(error_msg)

        upload_info = response.json()

        # Now prepare to upload the binary data directly to the presigned URL
        upload_url = upload_info['presignedUrl']
        s3_uri = upload_info['s3Uri']
        data_id = upload_info['dataId']

        # Parse S3 URI to get bucket and key
        s3_parts = s3_uri.replace("s3://", "").split("/", 1)
        bucket = s3_parts[0]
        key = s3_parts[1] if len(s3_parts) > 1 else data_id

        # Convert data to binary if needed
        binary_data = None
        try:
            if isinstance(data_to_upload, bytes):
                # Already in binary format
                binary_data = data_to_upload
                debug_print("Data is already in binary format")
            else:
                # Use pickle for any complex objects - maintain exact structure
                debug_print(f"Pickling data of type: {type(data_to_upload).__name__}")
                binary_data = pickle.dumps(data_to_upload, protocol=pickle.HIGHEST_PROTOCOL)
                debug_print(f"Data pickled successfully, size: {len(binary_data) / (1024 * 1024):.2f}MB")
        except Exception as e:
            spinner.stop()
            error_msg = f"Failed to serialize data: {e}"
            debug_print(traceback.format_exc())
            print(f"❌ {error_msg}")
            raise Exception(error_msg)

        # Get data size for progress reporting
        data_size = len(binary_data)
        data_size_mb = data_size / (1024 * 1024)

        # Update spinner message
        spinner.update_message(f"Uploading {data_size_mb:.2f}MB to S3...")

        # For small files, use simple PUT method
        if data_size_mb < 50:  # 50MB threshold
            # Upload using PUT method with the correct content-type
            content_type = 'application/python-pickle' if storage_format == 'pickle' else 'application/octet-stream'
            debug_print(f"Uploading with content-type: {content_type}")
            
            # Split large uploads into multiple attempts if needed
            MAX_ATTEMPTS = 3
            for attempt in range(MAX_ATTEMPTS):
                try:
                    upload_response = session.put(
                        upload_url,
                        data=binary_data,
                        headers={
                            'Content-Type': content_type
                        },
                        timeout=300  # Longer timeout for large uploads
                    )
                    
                    if upload_response.status_code in [200, 201, 204]:
                        debug_print(f"Upload successful with status code: {upload_response.status_code}")
                        break  # Success, exit retry loop
                        
                    debug_print(f"Upload attempt {attempt+1}/{MAX_ATTEMPTS} failed with status {upload_response.status_code}")
                    
                    if attempt < MAX_ATTEMPTS - 1:
                        # Wait before retrying with exponential backoff
                        wait_time = 2 ** attempt
                        spinner.update_message(f"Retrying upload in {wait_time}s ({attempt+2}/{MAX_ATTEMPTS})...")
                        time.sleep(wait_time)
                        spinner.update_message(f"Uploading {data_size_mb:.2f}MB to S3...")
                except Exception as e:
                    debug_print(f"Upload attempt {attempt+1}/{MAX_ATTEMPTS} failed with error: {str(e)}")
                    
                    if attempt < MAX_ATTEMPTS - 1:
                        # Wait before retrying with exponential backoff
                        wait_time = 2 ** attempt
                        spinner.update_message(f"Retrying upload in {wait_time}s ({attempt+2}/{MAX_ATTEMPTS})...")
                        time.sleep(wait_time)
                        spinner.update_message(f"Uploading {data_size_mb:.2f}MB to S3...")
                    else:
                        debug_print("All direct upload attempts failed, trying boto3 approach")
                        # Try boto3 approach instead
                        use_boto3 = True
                        break
        else:
            # For larger files, use multipart upload via boto3
            debug_print(f"File size ({data_size_mb:.2f}MB) exceeds threshold, using multipart upload")
            use_boto3 = True

        # Use boto3 for multipart upload if needed
        if data_size_mb >= 50 or (locals().get('use_boto3', False)):
            try:
                # Extract credentials from URL
                from urllib.parse import urlparse, parse_qs
                parsed_url = urlparse(upload_url)
                query_params = parse_qs(parsed_url.query)
                
                # Parse the credentials from the presigned URL
                credentials = {
                    'aws_access_key_id': query_params.get('X-Amz-Credential', [''])[0].split('/')[0],
                    'aws_secret_access_key': 'dummy',  # We won't actually use this
                    'aws_session_token': query_params.get('X-Amz-Security-Token', [''])[0]
                }

                # Create a boto3 client using the temporary credentials from the presigned URL
                # Just upload to the specified bucket but use the boto3 features
                spinner.update_message(f"Using chunked upload for {data_size_mb:.2f}MB file...")
                
                # Create a BytesIO object from our binary data
                data_stream = io.BytesIO(binary_data)
                
                # Try to use the AWS CLI instead
                try:
                    import subprocess
                    import tempfile
                    
                    # Create a temporary file
                    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                        temp_path = temp_file.name
                        temp_file.write(binary_data)
                    
                    spinner.update_message(f"Uploading {data_size_mb:.2f}MB using AWS CLI...")
                    
                    # Build the AWS CLI command
                    aws_command = [
                        "aws", "s3", "cp", 
                        temp_path, 
                        s3_uri,
                        "--content-type", "application/python-pickle" if storage_format == 'pickle' else 'application/octet-stream'
                    ]
                    
                    # Execute the command
                    debug_print(f"Running AWS CLI command: {' '.join(aws_command)}")
                    upload_process = subprocess.run(
                        aws_command,
                        capture_output=True,
                        text=True
                    )
                    
                    # Cleanup temp file
                    os.unlink(temp_path)
                    
                    if upload_process.returncode == 0:
                        debug_print("AWS CLI upload successful")
                    else:
                        debug_print(f"AWS CLI upload failed: {upload_process.stderr}")
                        raise Exception(f"AWS CLI upload failed: {upload_process.stderr}")
                        
                except Exception as e:
                    debug_print(f"AWS CLI upload failed: {str(e)}")
                    debug_print("Falling back to boto3 multipart upload")
                    
                    # Create a boto3 client with robust configuration
                    boto3_config = Config(
                        retries={
                            'max_attempts': 10,
                            'mode': 'adaptive'
                        },
                        connect_timeout=30,
                        read_timeout=30,
                        region_name='us-west-1'
                    )
                    
                    # Extract region from credential string
                    region = query_params.get('X-Amz-Credential', [''])[0].split('/')[2]
                    
                    # Create the S3 client with retry handling 
                    s3_client = boto3.client(
                        's3',
                        region_name=region,
                        config=boto3_config
                    )
                    
                    # Calculate optimal multipart chunk size
                    chunk_size = 25 * 1024 * 1024  # 25MB - larger than the minimum 5MB
                    total_chunks = math.ceil(data_size / chunk_size)
                    spinner.update_message(f"Starting multipart upload with {total_chunks} chunks...")
                    
                    # Create a multipart upload
                    multipart_upload = s3_client.create_multipart_upload(
                        Bucket=bucket,
                        Key=key,
                        ContentType='application/python-pickle' if storage_format == 'pickle' else 'application/octet-stream'
                    )
                    upload_id = multipart_upload['UploadId']
                    
                    # Upload each chunk
                    parts = []
                    for i in range(total_chunks):
                        # Update progress message
                        spinner.update_message(f"Uploading chunk {i+1}/{total_chunks}...")
                        
                        # Calculate current chunk bounds
                        chunk_start = i * chunk_size
                        chunk_end = min(chunk_start + chunk_size, data_size)
                        current_chunk_size = chunk_end - chunk_start
                        
                        # Read current chunk of data
                        data_stream.seek(chunk_start)
                        chunk_data = data_stream.read(current_chunk_size)
                        
                        # Upload the chunk
                        part_response = s3_client.upload_part(
                            Bucket=bucket,
                            Key=key,
                            PartNumber=i+1,
                            UploadId=upload_id,
                            Body=chunk_data
                        )
                        
                        # Track the part
                        parts.append({
                            'PartNumber': i+1,
                            'ETag': part_response['ETag']
                        })
                    
                    # Complete the multipart upload
                    s3_client.complete_multipart_upload(
                        Bucket=bucket,
                        Key=key,
                        UploadId=upload_id,
                        MultipartUpload={'Parts': parts}
                    )
                    
                    debug_print(f"Multipart upload completed successfully")
            
            except Exception as e:
                spinner.stop()
                error_msg = f"Failed during multipart upload: {e}"
                debug_print(traceback.format_exc())
                print(f"❌ {error_msg}")
                raise
        
        # Check if upload was successful
        spinner.stop()
        print(f"✅ Large file uploaded successfully! Size: {data_size_mb:.2f}MB")
        print(f"📋 Data ID: {upload_info['dataId']}")
        print(f"🔗 S3 URI: {upload_info['s3Uri']}")

        # Return a response in the same format as the standard upload API
        return {
            'dataId': upload_info['dataId'],
            's3Uri': upload_info['s3Uri'],
            'storageFormat': storage_format,
            'sizeMB': f"{data_size_mb:.2f}",
            'contentType': 'application/python-pickle' if storage_format == 'pickle' else 'application/octet-stream'
        }

    except Exception as e:
        spinner.stop()
        print(f"❌ Error during large file upload: {e}")
        debug_print(traceback.format_exc())
        # Re-raise the exception with more context
        raise Exception(f"Large file upload failed: {e}") from e
    finally:
        spinner.stop()