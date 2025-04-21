import requests
import traceback
import io
import time
from ...config import NERD_COMPUTE_ENDPOINT, DEBUG_MODE
from ...spinner import Spinner
from ...utils import debug_print
from .data_parsing_utils import deserialize_data

def fetch_large_file(data_id, api_key, max_retries=3, retry_delay=1):
    """
    Fetch a large file from NERD cloud storage.
    
    This function handles the download of large files:
    1. Gets a presigned URL for downloading
    2. Downloads the binary data
    3. Returns the raw binary data (caller is responsible for deserialization)
    
    Args:
        data_id: The data ID to fetch
        api_key: The NERD compute API key
        max_retries: Maximum number of retries on failure
        retry_delay: Delay between retries in seconds
        
    Returns:
        str: The raw downloaded data
    """
    if not data_id:
        raise ValueError("data_id is required to fetch a large file")
    
    spinner = Spinner(f"Fetching presigned URL for file (ID: {data_id})...")
    spinner.start()
    
    try:
        # Step 1: Get a presigned URL for downloading
        # Ensure the endpoint doesn't have a trailing slash before adding the path
        endpoint = NERD_COMPUTE_ENDPOINT.rstrip('/')
        url = f"{endpoint}/data/large"
        
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': api_key
        }
        
        params = {'dataId': data_id}
        
        # Try to get the presigned URL with retries
        response = None
        for attempt in range(max_retries):
            try:
                debug_print(f"Requesting download URL from: {url} for dataId: {data_id}")
                response = requests.get(url, headers=headers, params=params)
                if response.status_code == 200:
                    break
                    
                debug_print(f"Attempt {attempt+1}: Failed to get presigned URL with status {response.status_code}: {response.text}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
            except Exception as e:
                debug_print(f"Attempt {attempt+1}: Error getting presigned URL: {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
        
        if not response or response.status_code != 200:
            error_msg = f"Failed to get presigned URL after {max_retries} attempts"
            if response:
                error_msg += f": {response.status_code} - {response.text}"
            spinner.stop()
            print(f"❌ {error_msg}")
            raise ValueError(error_msg)
            
        download_info = response.json()
        presigned_url = download_info.get('presignedUrl')
        
        if not presigned_url:
            spinner.stop()
            error_msg = "No presigned URL found in the response"
            print(f"❌ {error_msg}")
            raise ValueError(error_msg)
            
        # Step 2: Download the file
        # Stop the current spinner and create a new one for downloading
        spinner.stop()
        spinner = Spinner(f"Downloading large file from S3...")
        spinner.start()
        
        # Try to download with retries
        download_response = None
        for attempt in range(max_retries):
            try:
                download_response = requests.get(presigned_url)
                if download_response.status_code == 200:
                    break
                    
                debug_print(f"Attempt {attempt+1}: Failed to download file with status {download_response.status_code}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
            except Exception as e:
                debug_print(f"Attempt {attempt+1}: Error downloading file: {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
        
        if not download_response or download_response.status_code != 200:
            error_msg = f"Failed to download file after {max_retries} attempts"
            if download_response:
                error_msg += f": {download_response.status_code}"
            spinner.stop()
            print(f"❌ {error_msg}")
            raise ValueError(error_msg)
            
        # Get the raw binary data
        raw_data = download_response.content
        
        # Step 3: Return the raw data (caller is responsible for deserialization)
        file_size_mb = len(raw_data) / (1024 * 1024)
        spinner.stop()
        print(f"✅ Large file downloaded successfully! Size: {file_size_mb:.2f}MB")
        
        # Return the response as a base64 string
        try:
            # We handle this as raw binary data
            return raw_data
        except Exception as e:
            debug_print(f"Error decoding data: {e}")
            return download_response.text
        
    except Exception as e:
        spinner.stop()
        print(f"❌ Error fetching large file: {e}")
        if DEBUG_MODE:
            traceback.print_exc()
        raise
    finally:
        spinner.stop()