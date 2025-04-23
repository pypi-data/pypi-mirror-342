import requests
import json
import io
import pickle
import traceback
from ...utils import debug_print
from ...spinner import Spinner

def fetch_large_file(data_id, api_key):
    """
    Handle download of large files from the cloud storage

    Args:
        data_id: The ID of the data to fetch
        api_key: The API key for authentication

    Returns:
        The fetched data (binary or parsed JSON)
    """
    # Set up the request
    spinner = Spinner(f"Getting presigned URL for large file download...")
    spinner.start()

    try:
        # First, get the presigned URL for download
        headers = {
            'x-api-key': api_key
        }

        response = requests.get(
            f'https://lbmoem9mdg.execute-api.us-west-1.amazonaws.com/prod/nerd-mega-compute/data/large?dataId={data_id}',
            headers=headers
        )

        if response.status_code != 200:
            spinner.stop()
            error_msg = f"Failed to get presigned URL for large file fetch: {response.text}"
            print(f"❌ {error_msg}")
            raise Exception(error_msg)

        download_info = response.json()

        # Now download the binary data directly from the presigned URL
        download_url = download_info['presignedUrl']
        content_type = download_info.get('contentType', 'application/octet-stream')
        content_length = download_info.get('contentLength', 0)
        size_mb = download_info.get('sizeMB', '?.??')

        # Update spinner message
        spinner.update_message(f"Downloading {size_mb}MB from presigned URL...")

        # Stream the download to handle large files efficiently
        download_response = requests.get(download_url, stream=True)

        if download_response.status_code != 200:
            spinner.stop()
            error_msg = f"Failed to download data from presigned URL: {download_response.text}"
            print(f"❌ {error_msg}")
            raise Exception(error_msg)

        # Use BytesIO for memory efficiency
        content = io.BytesIO()

        # Use chunks to avoid loading entire file into memory at once
        chunk_size = 8192  # 8KB chunks
        for chunk in download_response.iter_content(chunk_size=chunk_size):
            if chunk:  # filter out keep-alive new chunks
                content.write(chunk)

        content.seek(0)
        binary_data = content.read()

        spinner.stop()
        print(f"✅ Large file downloaded successfully! Size: {size_mb}MB")
        print(f"[DOWNLOAD_DEBUG] Download completed, content type: {content_type}")
        print(f"[DOWNLOAD_DEBUG] Binary data size: {len(binary_data) / (1024 * 1024):.2f}MB")

        # First try to deserialize as pickle if it's potentially a pickle file
        if content_type in ('application/python-pickle', 'application/octet-stream'):
            try:
                print(f"[DOWNLOAD_DEBUG] Attempting pickle deserialization")
                result = pickle.loads(binary_data)
                print(f"[DOWNLOAD_DEBUG] Successfully deserialized pickled object of type: {type(result).__name__}")
                
                # Print additional information about the result for debugging
                if hasattr(result, '__dict__'):
                    print(f"[DOWNLOAD_DEBUG] Object attributes: {dir(result)[:20]}")
                elif isinstance(result, dict):
                    print(f"[DOWNLOAD_DEBUG] Dictionary keys: {list(result.keys())[:20] if result else 'empty'}")
                elif hasattr(result, 'shape'):
                    print(f"[DOWNLOAD_DEBUG] Object shape: {result.shape}")
                
                return result
            except Exception as e:
                print(f"[DOWNLOAD_DEBUG] Pickle deserialization failed: {str(e)}")
                print(traceback.format_exc())
                # Continue to try other formats if pickle fails
        
        # Try to detect and parse specific content types
        if content_type == 'application/json' or _looks_like_json(binary_data):
            try:
                # Try to decode as JSON
                decoded_text = binary_data.decode('utf-8')
                print(f"[DOWNLOAD_DEBUG] Attempting JSON deserialization")

                # Check if it's a JSON string that needs to be parsed twice
                # (This happens when JSON is stored as a string inside JSON)
                if (decoded_text.startswith('"[') and decoded_text.endswith(']"')) or \
                   (decoded_text.startswith('"{') and decoded_text.endswith('}"')):
                    # This is a JSON string that contains escaped JSON
                    # First parse the outer JSON string
                    unescaped_json_str = json.loads(decoded_text)
                    # Then parse the inner JSON data
                    result = json.loads(unescaped_json_str)
                    print(f"[DOWNLOAD_DEBUG] Successfully deserialized nested JSON")
                    return result
                else:
                    # Normal JSON, parse once
                    result = json.loads(decoded_text)
                    print(f"[DOWNLOAD_DEBUG] Successfully deserialized JSON")
                    return result
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                print(f"[DOWNLOAD_DEBUG] JSON deserialization failed: {str(e)}")
                # If it fails to parse as JSON, fall through to other methods

        # For text-based content types, try to decode as text
        if content_type.startswith('text/') or _looks_like_text(binary_data):
            try:
                # Try to decode as text
                text_data = binary_data.decode('utf-8')
                print(f"[DOWNLOAD_DEBUG] Successfully decoded as text, length: {len(text_data)}")

                # Check if the text looks like JSON
                if (text_data.startswith('{') and text_data.endswith('}')) or \
                   (text_data.startswith('[') and text_data.endswith(']')):
                    try:
                        result = json.loads(text_data)
                        print(f"[DOWNLOAD_DEBUG] Text successfully parsed as JSON")
                        return result
                    except json.JSONDecodeError:
                        print(f"[DOWNLOAD_DEBUG] Text is not valid JSON")

                return text_data
            except UnicodeDecodeError as e:
                print(f"[DOWNLOAD_DEBUG] Text decoding failed: {str(e)}")
                # If it fails to decode as text, fall through to binary

        # Return raw binary for other types
        print(f"[DOWNLOAD_DEBUG] Returning raw binary data as no deserialization method succeeded")
        return binary_data

    except Exception as e:
        spinner.stop()
        print(f"❌ Error during large file download: {e}")
        print(traceback.format_exc())
        raise
    finally:
        spinner.stop()

def _looks_like_json(binary_data):
    """
    Check if binary data looks like it might be JSON

    Args:
        binary_data: Binary data to check

    Returns:
        bool: True if the data appears to be JSON
    """
    # Check just the beginning of the data to avoid decoding large files completely
    sample = binary_data[:100].strip()
    try:
        # Check if it starts with a JSON object or array
        return (sample.startswith(b'{') and b'}' in binary_data[-10:]) or \
               (sample.startswith(b'[') and b']' in binary_data[-10:]) or \
               (sample.startswith(b'"[') and sample.find(b'\\{') > 0) or \
               (sample.startswith(b'"{') and sample.find(b'\\{') > 0)
    except:
        return False

def _looks_like_text(binary_data):
    """
    Check if binary data looks like it might be text

    Args:
        binary_data: Binary data to check

    Returns:
        bool: True if the data appears to be text
    """
    # Check a sample of the data
    sample = binary_data[:1000]

    # Try to decode as UTF-8
    try:
        sample.decode('utf-8')
        return True
    except UnicodeDecodeError:
        pass

    # Check if most bytes are in the printable ASCII range
    printable_count = sum(32 <= b <= 126 for b in sample)
    return printable_count > 0.8 * len(sample) if sample else False