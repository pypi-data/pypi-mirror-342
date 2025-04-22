import requests
import json
import pickle
from ...utils import debug_print
from ...spinner import Spinner

def upload_large_file(data_to_upload, api_key, storage_format=None):
    """
    Handle upload of large files to the cloud storage

    Args:
        data_to_upload: The data to upload
        api_key: The API key for authentication
        storage_format: Format to store data (binary or json)

    Returns:
        dict: Information about the uploaded data
    """
    # Determine storage format if not specified
    if storage_format is None:
        storage_format = 'binary' if isinstance(data_to_upload, bytes) else 'json'

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
        binary_data = data_to_upload
        if not isinstance(data_to_upload, bytes):
            try:
                if storage_format == 'json':
                    try:
                        binary_data = json.dumps(data_to_upload).encode('utf-8')
                    except (TypeError, OverflowError):
                        # If not JSON serializable, convert to string representation
                        binary_data = str(data_to_upload).encode('utf-8')
                else:
                    # Use pickle for any complex objects
                    binary_data = pickle.dumps(data_to_upload)
            except Exception as e:
                spinner.stop()
                error_msg = f"Failed to serialize data: {e}"
                print(f"❌ {error_msg}")
                raise Exception(error_msg)

        # Get data size for progress reporting
        data_size = len(binary_data)
        data_size_mb = data_size / (1024 * 1024)

        # Update spinner message
        spinner.update_message(f"Uploading {data_size_mb:.2f}MB to presigned URL...")

        # Upload using PUT method with the correct content-type
        upload_response = requests.put(
            upload_url,
            data=binary_data,
            headers={
                'Content-Type': 'application/octet-stream'
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
            'sizeMB': f"{data_size_mb:.2f}"
        }

    except Exception as e:
        spinner.stop()
        print(f"❌ Error during large file upload: {e}")
        raise
    finally:
        spinner.stop()