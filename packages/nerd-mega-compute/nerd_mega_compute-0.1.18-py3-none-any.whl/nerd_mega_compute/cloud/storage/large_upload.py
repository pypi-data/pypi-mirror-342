import requests
import traceback
import io
import os
import tempfile
import base64
import cloudpickle

from ...config import NERD_COMPUTE_ENDPOINT, DEBUG_MODE
from ...spinner import Spinner
from ...utils import debug_print
from .data_parsing_utils import serialize_data
from ..auth import get_api_key

def upload_large_file(data_to_upload, metadata=None):
    """
    Upload large data to NERD cloud storage.
    
    This function handles the chunked upload process for large files:
    1. Serializes the data consistently with serialize_data
    2. Gets a presigned URL for uploading
    3. Performs the chunked upload
    
    Args:
        data_to_upload: The data to upload (any Python object)
        metadata: Optional metadata dictionary
        
    Returns:
        dict: Response from the upload service including dataId
    """
    api_key = get_api_key()
    if not api_key:
        raise ValueError(
            "API_KEY is not set. Please set it using:\n"
            "1. Create a .env file with NERD_COMPUTE_API_KEY=your_key_here\n"
            "2. Or call set_nerd_compute_api_key('your_key_here')"
        )

    spinner = Spinner("Preparing large file upload...")
    spinner.start()

    try:
        # Step 1: Prepare data for upload using our improved serialization
        binary_data, format_metadata = serialize_data(data_to_upload)
        
        # Ensure binary_data is bytes
        if not isinstance(binary_data, bytes):
            debug_print(f"Warning: serialized data is not bytes but {type(binary_data)}")
            if isinstance(binary_data, str):
                binary_data = binary_data.encode('utf-8')
        
        # Get the size of the binary data
        file_size = len(binary_data)
        debug_print(f"Serialized data size: {file_size} bytes")
        
        # Merge user metadata with format metadata
        if metadata is None:
            metadata = {}
        metadata.update(format_metadata)
        
        # Step 2: Get a presigned URL for uploading
        debug_print(f"Getting presigned URL for uploading {file_size} bytes")
        
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': api_key
        }
        
        # Include metadata about our serialization format
        upload_request = {
            'storageFormat': format_metadata['format'],
            'dataType': 'application/octet-stream',
            'fileSize': file_size,
            'metadata': metadata
        }
        
        # Ensure the endpoint doesn't have a trailing slash before adding the path
        endpoint = NERD_COMPUTE_ENDPOINT.rstrip('/')
        url = f"{endpoint}/data/large"
        
        debug_print(f"Requesting presigned URL from: {url}")
        response = requests.post(
            url,
            json=upload_request,
            headers=headers
        )
        
        if response.status_code != 200:
            error_msg = f"Failed to get presigned URL with status {response.status_code}: {response.text}"
            spinner.stop()
            print(f"❌ {error_msg}")
            raise ValueError(error_msg)
            
        presigned_info = response.json()
        
        debug_print(f"Received presigned URL: {presigned_info.get('presignedUrl', '')[:60]}...")
        
        # Step 3: Upload the file using the presigned URL
        # Stop the current spinner and create a new one with the upload message
        spinner.stop()
        spinner = Spinner("Uploading large file...")
        spinner.start()
        
        # Create a file-like object from binary data
        data_io = io.BytesIO(binary_data)
        
        # Upload the file using the presigned URL - critical to use the correct content type
        upload_headers = {
            'Content-Type': 'application/octet-stream',
            'Content-Length': str(file_size)
        }
        
        debug_print(f"Uploading {file_size} bytes to S3 with content type: application/octet-stream")
        upload_response = requests.put(
            presigned_info['presignedUrl'],
            data=data_io,
            headers=upload_headers
        )
        
        if upload_response.status_code not in [200, 201, 204]:
            error_msg = f"Failed to upload file with status {upload_response.status_code}: {upload_response.text}"
            spinner.stop()
            print(f"❌ {error_msg}")
            raise ValueError(error_msg)
            
        # Step 4: Return the upload details
        result = {
            'dataId': presigned_info.get('dataId'),
            's3Uri': presigned_info.get('s3Uri'),
            'sizeMB': round(file_size / (1024 * 1024), 2),
            'metadata': metadata,
            'storageFormat': format_metadata['format']
        }
        
        spinner.stop()
        size_mb = result.get('sizeMB', '?')
        print(f"✅ Large file uploaded successfully! Size: {size_mb}MB")
        print(f"📋 Data ID: {result.get('dataId', '?')}")
        print(f"🔗 S3 URI: {result.get('s3Uri', '?')}")
        
        return result
    
    except Exception as e:
        spinner.stop()
        print(f"❌ Error uploading large file: {e}")
        if DEBUG_MODE:
            traceback.print_exc()
        raise
    finally:
        spinner.stop()