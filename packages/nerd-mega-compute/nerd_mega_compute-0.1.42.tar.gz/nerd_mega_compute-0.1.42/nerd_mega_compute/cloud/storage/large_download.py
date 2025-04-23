import requests
import json
import io
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

        # Try to detect and parse specific content types
        if content_type == 'application/json' or (
            content_type == 'application/octet-stream' and _looks_like_json(binary_data)):
            try:
                # Try to decode as JSON
                decoded_text = binary_data.decode('utf-8')

                # Check if it's a JSON string that needs to be parsed twice
                # (This happens when JSON is stored as a string inside JSON)
                if (decoded_text.startswith('"[') and decoded_text.endswith(']"')) or \
                   (decoded_text.startswith('"{') and decoded_text.endswith('}"')):
                    # This is a JSON string that contains escaped JSON
                    # First parse the outer JSON string
                    unescaped_json_str = json.loads(decoded_text)
                    # Then parse the inner JSON data
                    return json.loads(unescaped_json_str)
                else:
                    # Normal JSON, parse once
                    return json.loads(decoded_text)
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                debug_print(f"Error parsing JSON: {e}")
                # If it fails to parse as JSON, return the binary data
                pass

        # For text-based content types, try to decode as text
        if content_type.startswith('text/') or _looks_like_text(binary_data):
            try:
                # Try to decode as text
                text_data = binary_data.decode('utf-8')

                # Check if the text looks like JSON
                if (text_data.startswith('{') and text_data.endswith('}')) or \
                   (text_data.startswith('[') and text_data.endswith(']')):
                    try:
                        return json.loads(text_data)
                    except json.JSONDecodeError:
                        pass

                return text_data
            except UnicodeDecodeError:
                # If it fails to decode as text, return the binary data
                pass

        # Return raw binary for other types
        return binary_data

    except Exception as e:
        spinner.stop()
        print(f"❌ Error during large file download: {e}")
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