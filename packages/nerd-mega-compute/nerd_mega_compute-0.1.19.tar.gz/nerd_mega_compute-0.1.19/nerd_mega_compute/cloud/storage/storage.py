import requests
import json
import base64
import traceback
import zlib
import pickle

from ...config import NERD_COMPUTE_ENDPOINT, DEBUG_MODE
from ...spinner import Spinner
from ...utils import debug_print
from .large_upload import upload_large_file
from .large_download import fetch_large_file
from .data_size_utils import is_large_data
from .data_parsing_utils import serialize_data, deserialize_data
from ..auth import get_api_key

def upload_nerd_cloud_storage(data_to_upload, metadata=None):
    """
    Uploads data to cloud storage.

    Args:
        data_to_upload: Data to be uploaded
        metadata: Optional metadata to include with the upload

    Returns:
        dict: Response from the cloud storage service
    """
    print("If large data result", is_large_data(data_to_upload))

    # Check if data is large and use appropriate upload method
    if is_large_data(data_to_upload):
        debug_print("Data detected as large, using chunked upload method")
        return upload_large_file(data_to_upload, metadata)

    # Regular upload for smaller data
    api_key = get_api_key()
    if not api_key:
        raise ValueError(
            "API_KEY is not set. Please set it using:\n"
            "1. Create a .env file with NERD_COMPUTE_API_KEY=your_key_here\n"
            "2. Or call set_nerd_compute_api_key('your_key_here')"
        )

    spinner = Spinner("Uploading data to Nerd Cloud Storage...")
    spinner.start()

    try:
        # Use our consistent serialization approach
        serialized_data, format_metadata = serialize_data(data_to_upload)

        # Merge user metadata with format metadata
        if metadata is None:
            metadata = {}
        metadata.update(format_metadata)

        request_payload = {
            'data': serialized_data,
            'storageFormat': format_metadata['format'],
            'dataType': 'application/octet-stream',
            'metadata': metadata
        }

        headers = {
            "Content-Type": "application/json",
            "x-api-key": api_key,
        }

        endpoint = f"{NERD_COMPUTE_ENDPOINT}/data"

        debug_print(f"Sending data upload request to {endpoint}")
        debug_print(f"Storage format: {format_metadata['format']}")

        response = requests.post(
            endpoint,
            headers=headers,
            json=request_payload,
            timeout=30
        )

        debug_print(f"Upload response status: {response.status_code}")

        if response.status_code != 200:
            spinner.stop()
            error_msg = f"Upload failed with status {response.status_code}"
            try:
                error_data = response.json()
                error_details = error_data.get("error", "") or error_data.get("details", "")
                if error_details:
                    error_msg += f": {error_details}"
            except Exception:
                error_msg += f": {response.text}"

            print(f"❌ {error_msg}")
            raise ValueError(error_msg)

        result = response.json()
        spinner.stop()
        size_mb = result.get('sizeMB', '?')
        print(f"✅ Data uploaded successfully! Size: {size_mb}MB")
        print(f"📋 Data ID: {result.get('dataId', '?')}")
        print(f"🔗 S3 URI: {result.get('s3Uri', '?')}")

        return result

    except Exception as e:
        spinner.stop()
        print(f"❌ Error uploading to cloud storage: {e}")
        if DEBUG_MODE:
            traceback.print_exc()
        raise
    finally:
        spinner.stop()

def fetch_nerd_cloud_storage(data_id_or_response):
    """
    Fetch data from NERD cloud storage

    Args:
        data_id_or_response: Either the dataId string or the complete upload response object

    Returns:
        The fetched data, automatically decoded and deserialized if needed
    """
    if isinstance(data_id_or_response, dict) and 'dataId' in data_id_or_response:
        data_id = data_id_or_response['dataId']
        # Check if this is a large file response
        if data_id_or_response.get('sizeMB') or 'storageFormat' in data_id_or_response:
            try:
                # Check if it's a large file by either size or format
                size_mb = 0
                try:
                    size_mb = float(data_id_or_response.get('sizeMB', '0'))
                except (ValueError, TypeError):
                    pass

                storage_format = data_id_or_response.get('storageFormat', '')

                # If size > 10MB or explicitly has a storage format, use large file fetch
                if size_mb >= 10 or storage_format:
                    debug_print(f"Detected large file (size: {size_mb}MB, format: {storage_format}), using large file fetch API")
                    api_key = get_api_key()
                    if not api_key:
                        raise ValueError(
                            "API_KEY is not set. Please set it using:\n"
                            "1. Create a .env file with NERD_COMPUTE_API_KEY=your_key_here\n"
                            "2. Or call set_nerd_compute_api_key('your_key_here')"
                        )

                    # Get raw data from large file fetch
                    raw_data = fetch_large_file(data_id, api_key)

                    # Process the raw data
                    metadata = data_id_or_response.get('metadata', {})
                    return deserialize_data(raw_data, metadata)
            except (ValueError, TypeError) as e:
                debug_print(f"Error checking if large file: {e}")
    else:
        data_id = data_id_or_response

    api_key = get_api_key()
    if not api_key:
        raise ValueError(
            "API_KEY is not set. Please set it using:\n"
            "1. Create a .env file with NERD_COMPUTE_API_KEY=your_key_here\n"
            "2. Or call set_nerd_compute_api_key('your_key_here')"
        )

    if not data_id:
        raise ValueError("Either data_id or s3_uri must be provided to fetch data")

    params = {}
    if data_id:
        params["dataId"] = data_id

    spinner = Spinner("Fetching data from Nerd Cloud Storage...")
    spinner.start()

    try:
        endpoint = f"{NERD_COMPUTE_ENDPOINT}/data"
        headers = {
            "x-api-key": api_key
        }

        debug_print(f"Sending data fetch request to {endpoint} with params {params}")
        response = requests.get(
            endpoint,
            headers=headers,
            params=params,
            timeout=30
        )

        debug_print(f"Fetch response status: {response.status_code}")

        if response.status_code != 200:
            error_msg = f"Fetch failed with status {response.status_code}: {response.text}"

            # Try large file API as a fallback
            try:
                debug_print("Attempting to fetch using large file API as fallback...")
                raw_data = fetch_large_file(data_id, api_key)

                # Try to deserialize the raw data
                return deserialize_data(raw_data)
            except Exception as e:
                debug_print(f"Large file API fallback failed: {e}")

            # If all fallbacks failed, now show the error
            spinner.stop()
            print(f"❌ {error_msg}")
            raise ValueError(error_msg)

        result = response.json()

        if "contentLength" in result and "presignedUrl" in result:
            debug_print("Detected large file metadata in response, using large file fetch API")
            spinner.stop()
            raw_data = fetch_large_file(data_id, api_key)
            return deserialize_data(raw_data, result.get('metadata', {}))

        if "data" in result:
            data = result["data"]
            metadata = result.get("metadata", {})
            storage_format = result.get("storageFormat", "json")

            # Add storage format to metadata if not present
            if "format" not in metadata:
                metadata["format"] = storage_format

            # Deserialize the data
            deserialized_data = deserialize_data(data, metadata)

            spinner.stop()

            content_type = metadata.get("content-type", "unknown")
            size_mb = metadata.get("size-mb", "?")
            print(f"✅ Data fetched successfully! Size: {size_mb}MB, Type: {content_type}")

            return deserialized_data
        else:
            spinner.stop()
            print(f"❓ Unexpected response format. No data found in the response.")
            return result

    except Exception as e:
        spinner.stop()
        print(f"❌ Error fetching from cloud storage: {e}")
        if DEBUG_MODE:
            traceback.print_exc()
        raise
    finally:
        spinner.stop()

def fetch_nerd_data_reference(reference_obj):
    """
    Convenience function to fetch data from a cloud storage reference.

    This is useful when working with large data objects that have been replaced
    with references during cloud computation.

    Args:
        reference_obj (dict): A reference object with a __nerd_data_reference key

    Returns:
        The fetched data, automatically deserialized based on its format
    """
    if not isinstance(reference_obj, dict):
        return reference_obj

    if "__nerd_data_reference" in reference_obj:
        data_id = reference_obj["__nerd_data_reference"]
        print(f"Fetching data reference: {data_id}")
        return fetch_nerd_cloud_storage(data_id)

    return reference_obj
