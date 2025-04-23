import requests
import json
import pickle
from ...utils import debug_print
from ...spinner import Spinner
import traceback

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
        # First, get the presigned URL for upload
        headers = {
            'x-api-key': api_key
        }

        response = requests.post(
            'https://lbmoem9mdg.execute-api.us-west-1.amazonaws.com/prod/nerd-mega-compute/data/large',
            headers=headers
        )

        if response.status_code != 200:
            spinner.stop()
            error_msg = f"Failed to get presigned URL for large file upload: {response.text}"
            print(f"❌ {error_msg}")
            raise Exception(error_msg)

        upload_info = response.json()

        # Now prepare to upload the binary data directly to the presigned URL
        upload_url = upload_info['presignedUrl']

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
        spinner.update_message(f"Uploading {data_size_mb:.2f}MB to presigned URL...")

        # Upload using PUT method with the correct content-type
        content_type = 'application/python-pickle' if storage_format == 'pickle' else 'application/octet-stream'
        debug_print(f"Uploading with content-type: {content_type}")
        
        upload_response = requests.put(
            upload_url,
            data=binary_data,
            headers={
                'Content-Type': content_type
            }
        )

        if upload_response.status_code not in [200, 201, 204]:
            spinner.stop()
            error_msg = f"Failed to upload data to presigned URL: {upload_response.text}"
            print(f"❌ {error_msg}")
            raise Exception(error_msg)

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
            'contentType': content_type
        }

    except Exception as e:
        spinner.stop()
        print(f"❌ Error during large file upload: {e}")
        debug_print(traceback.format_exc())
        raise
    finally:
        spinner.stop()