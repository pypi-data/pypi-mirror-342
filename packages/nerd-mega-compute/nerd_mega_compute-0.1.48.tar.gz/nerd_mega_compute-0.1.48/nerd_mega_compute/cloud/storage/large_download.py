import requests
import json
import io
import pickle
import traceback
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from ...utils import debug_print
from ...spinner import Spinner

def fetch_large_file(data_id, api_key=None):
    """
    Fetch a large file from NERD cloud storage using the large file API
    
    Args:
        data_id (str): The data ID to fetch
        api_key (str, optional): API key for authentication. If not provided, will use the configured key.
        
    Returns:
        The downloaded data, automatically deserialized based on content type
    """
    if not api_key:
        from ..auth import get_api_key
        api_key = get_api_key()
        if not api_key:
            raise ValueError(
                "API_KEY is not set. Please set it using:\n"
                "1. Create a .env file with NERD_COMPUTE_API_KEY=your_key_here\n"
                "2. Or call set_nerd_compute_api_key('your_key_here')"
            )
            
    spinner = Spinner("Downloading large file from Nerd Cloud Storage...")
    spinner.start()
            
    try:
        # Fetch the pre-signed URL for the specified data ID
        endpoint = "https://lbmoem9mdg.execute-api.us-west-1.amazonaws.com/prod/nerd-mega-compute/data/large"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": api_key
        }
        params = {"dataId": data_id}
        
        debug_print(f"Requesting pre-signed URL for data ID: {data_id}")
        
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        
        response = session.get(endpoint, headers=headers, params=params, timeout=30)
        
        if response.status_code != 200:
            error_msg = f"Failed to get pre-signed URL with status {response.status_code}: {response.text}"
            spinner.stop()
            print(f"❌ {error_msg}")
            raise ValueError(error_msg)
            
        data = response.json()
        presigned_url = data.get("presignedUrl")
        content_type = data.get("contentType", "application/octet-stream")
        size_mb = data.get("contentLength", 0) / (1024 * 1024)
        
        if not presigned_url:
            spinner.stop()
            error_msg = "No presigned URL found in the response"
            print(f"❌ {error_msg}")
            raise ValueError(error_msg)
            
        debug_print(f"Downloading file with pre-signed URL, size: {size_mb:.2f}MB, content type: {content_type}")
        
        # Download the binary data from the pre-signed URL
        start_time = time.time()
        download_response = session.get(presigned_url, timeout=300)  # Longer timeout for large downloads
        
        if download_response.status_code != 200:
            spinner.stop()
            error_msg = f"Failed to download data with status {download_response.status_code}"
            print(f"❌ {error_msg}")
            raise ValueError(error_msg)
            
        binary_data = download_response.content
        actual_size_mb = len(binary_data) / (1024 * 1024)
        download_time = time.time() - start_time
        
        spinner.stop()
        print(f"✅ Large file downloaded successfully! Size: {actual_size_mb:.2f}MB")
        debug_print(f"Download completed, content type: {content_type}")
        debug_print(f"Binary data size: {actual_size_mb:.2f}MB")
        
        # Determine if this is likely binary data that should not be deserialized
        is_likely_pure_binary = False
        
        # Check the first few bytes for common binary file signatures
        if len(binary_data) > 8:
            # Check for common binary signatures
            if (binary_data.startswith(b'\x00\x01\x02\x03') or 
                binary_data.startswith(b'\x00\x00\x00') or 
                # Lots of null bytes is a good indicator of raw binary data
                binary_data.count(b'\x00') > len(binary_data) * 0.25):
                debug_print("Detected likely pure binary data based on byte pattern")
                is_likely_pure_binary = True
                
        # First, handle based on content type
        if content_type == "application/python-pickle":
            # This is explicitly marked as pickle, try to deserialize
            try:
                debug_print("Attempting pickle deserialization")
                result = pickle.loads(binary_data)
                debug_print(f"Successfully deserialized pickled object of type: {type(result).__name__}")
                return result
            except Exception as e:
                debug_print(f"Pickle deserialization failed: {str(e)}")
                # Fall through to additional handling
        
        # For binary that's not marked as pickle or if pickle fails
        elif content_type == "application/octet-stream" and not is_likely_pure_binary:
            # Try pickle deserialization for octet-stream only if it doesn't look like pure binary
            try:
                debug_print("Attempting pickle deserialization")
                result = pickle.loads(binary_data)
                debug_print(f"Successfully deserialized pickled object of type: {type(result).__name__}")
                return result
            except Exception as e:
                debug_print(f"Pickle deserialization failed: {str(e)}")
                # Fall through to additional handling
        
        # For likely pure binary data, skip pickle deserialization attempt
        elif is_likely_pure_binary:
            debug_print("Skipping deserialization for pure binary data")
            return binary_data
            
        # For JSON content
        if content_type == "application/json":
            try:
                debug_print("Attempting JSON parsing")
                text = binary_data.decode('utf-8')
                result = json.loads(text)
                debug_print("Successfully parsed JSON data")
                return result
            except Exception as e:
                debug_print(f"JSON parsing failed: {str(e)}")
                # Fall through to text handling
                
        # Try to decode as UTF-8 text
        try:
            text = binary_data.decode('utf-8')
            debug_print(f"Successfully decoded as text, length: {len(text)}")
            
            # If it looks like JSON, try to parse it
            if text.strip().startswith('{') or text.strip().startswith('['):
                try:
                    result = json.loads(text)
                    debug_print("Successfully parsed JSON data from text")
                    return result
                except:
                    pass
                    
            # Return as text if it's valid UTF-8
            return text
        except UnicodeDecodeError:
            # Not valid UTF-8, return as binary
            debug_print("Not valid UTF-8 text, returning as binary")
            
        # Default to returning the raw binary data
        return binary_data
            
    except Exception as e:
        spinner.stop()
        print(f"❌ Error downloading large file: {str(e)}")
        if DEBUG_MODE:
            traceback.print_exc()
        raise
    finally:
        spinner.stop()