import requests
import traceback
import io
import base64

from ...config import NERD_COMPUTE_ENDPOINT, DEBUG_MODE
from ...spinner import Spinner
from ...utils import debug_print
from .data_parsing_utils import serialize_data
from ..auth import get_api_key

def upload_large_file(data_to_upload, metadata=None):
    """
    Upload large data to NERD cloud storage using a simplified approach.

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
        # Step 1: Serialize the data using our simplified approach
        serialized_data, format_metadata = serialize_data(data_to_upload)

        # Convert the base64 string back to binary for upload
        binary_data = base64.b64decode(serialized_data)
        file_size = len(binary_data)

        debug_print(f"Serialized data size: {file_size/1024/1024:.2f} MB")

        # Merge user metadata with format metadata
        if metadata is None:
            metadata = {}
        metadata.update(format_metadata)

        # Step 2: Get a presigned URL for uploading
        spinner.stop()
        spinner = Spinner(f"Getting presigned URL for upload...")
        spinner.start()

        headers = {
            'Content-Type': 'application/json',
            'x-api-key': api_key
        }

        # Create upload request
        upload_request = {
            'storageFormat': format_metadata['format'],
            'dataType': 'application/octet-stream',
            'fileSize': file_size,
            'metadata': metadata
        }

        # Request a presigned URL
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

        # Step 3: Upload the binary data to S3
        spinner.stop()
        spinner = Spinner("Uploading data to S3...")
        spinner.start()

        # Create a file-like object from binary data
        data_io = io.BytesIO(binary_data)

        # Upload using the presigned URL
        upload_response = requests.put(
            presigned_info['presignedUrl'],
            data=data_io,
            headers={'Content-Type': 'application/octet-stream'}
        )

        if upload_response.status_code not in [200, 201, 204]:
            error_msg = f"Failed to upload file with status {upload_response.status_code}: {upload_response.text}"
            spinner.stop()
            print(f"❌ {error_msg}")
            raise ValueError(error_msg)

        # Return the upload details
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