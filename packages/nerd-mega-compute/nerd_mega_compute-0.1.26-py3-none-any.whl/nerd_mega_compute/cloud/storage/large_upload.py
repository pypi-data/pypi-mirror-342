import requests
import traceback
import io
import os
import tempfile
import pickle
import base64
import zlib
import numpy as np

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
        # Step 1: Prepare data for upload - serialize consistently
        serialized_data, format_metadata = serialize_data(data_to_upload)

        # Merge user metadata with format metadata
        if metadata is None:
            metadata = {}
        metadata.update(format_metadata)

        # Convert the serialized string back to binary for upload
        binary_data = base64.b64decode(serialized_data)
        file_size = len(binary_data)

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

        debug_print("Requesting presigned URL...")
        response = requests.post(
            f"{NERD_COMPUTE_ENDPOINT}/data/upload",
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
        spinner.update_text("Uploading large file...")

        # Create a file-like object from binary data
        data_io = io.BytesIO(binary_data)

        # Upload the file using the presigned URL
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

        # Step 4: Return the upload details
        result = {
            'dataId': presigned_info.get('dataId'),
            's3Uri': presigned_info.get('s3Uri'),
            'sizeMB': round(file_size / (1024 * 1024), 2)
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