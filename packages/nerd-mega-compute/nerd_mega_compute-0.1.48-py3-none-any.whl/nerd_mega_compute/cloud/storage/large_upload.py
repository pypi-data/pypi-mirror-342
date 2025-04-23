import requests
import json
import pickle
import os
import io
import sys
import time
import tempfile
import uuid
from ...utils import debug_print
from ...spinner import Spinner
import traceback
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from tqdm import tqdm

# Constants for optimizing large astronomical data uploads
MAX_UPLOAD_SIZE = 60 * 1024 * 1024 * 1024  # Support up to 60GB
CHUNK_SIZE = 16 * 1024 * 1024  # 16MB chunks
MAX_RETRIES = 10
RETRY_BACKOFF = 1.5
CONNECTION_TIMEOUT = 30
READ_TIMEOUT = 1800  # 30 minutes for large dataset reading
UPLOAD_TIMEOUT = 3600  # 1 hour for extremely large uploads

# Create a requests session with robust retry logic for astronomical data
def create_robust_session():
    """Create a requests session with improved retry logic and connection handling"""
    session = requests.Session()
    
    # Configure robust retry strategy
    retry_strategy = Retry(
        total=MAX_RETRIES,
        backoff_factor=RETRY_BACKOFF,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "PUT", "DELETE", "POST", "OPTIONS", "HEAD"],
        respect_retry_after_header=True
    )
    
    # Configure adapter with retry strategy and longer timeouts
    adapter = HTTPAdapter(
        max_retries=retry_strategy,
        pool_connections=10,
        pool_maxsize=10,
        pool_block=False
    )
    
    # Mount adapter to both http and https
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session

class TqdmUpTo(tqdm):
    """Alternative tqdm class for tracking upload progress of large astronomical data."""
    def update_to(self, current, total=None):
        if total is not None:
            self.total = total
        self.update(current - self.n)

def optimize_data_for_upload(data_to_upload):
    """Pre-process data to optimize for large astronomical data uploads"""
    # If the data is already bytes, return it directly
    if isinstance(data_to_upload, bytes):
        return data_to_upload, 'binary'
    
    # For large astronomical data (dataframes, fits, etc.) use the highest protocol
    debug_print(f"Optimizing large astronomical data of type: {type(data_to_upload).__name__}")
    try:
        binary_data = pickle.dumps(data_to_upload, protocol=pickle.HIGHEST_PROTOCOL)
        return binary_data, 'pickle'
    except Exception as e:
        debug_print(f"Standard pickle failed: {str(e)}")
        # For extremely large numpy arrays or specialized astronomical data structures
        # Try more efficient serialization if possible
        try:
            import numpy as np
            if isinstance(data_to_upload, np.ndarray):
                debug_print("Using numpy-optimized serialization")
                buffer = io.BytesIO()
                np.save(buffer, data_to_upload, allow_pickle=True)
                buffer.seek(0)
                return buffer.getvalue(), 'numpy'
        except (ImportError, Exception) as e:
            debug_print(f"Numpy optimization failed: {str(e)}")
        
        # Fall back to standard pickle with error
        raise Exception(f"Failed to serialize large astronomical data: {e}")

def get_memory_optimized_temp_file(binary_data, prefix="astro_data_"):
    """Create a temporary file for large astronomical data to minimize memory usage"""
    # Generate unique temp filename
    temp_file_path = os.path.join(
        tempfile.gettempdir(), 
        f"{prefix}{uuid.uuid4().hex}.tmp"
    )
    
    # Write data to file in chunks to avoid memory issues
    chunk_size = 64 * 1024 * 1024  # 64MB chunks for writing
    with open(temp_file_path, 'wb') as f:
        for i in range(0, len(binary_data), chunk_size):
            chunk = binary_data[i:i+chunk_size]
            f.write(chunk)
            # Let Python GC collect the chunk immediately
            del chunk
    
    return temp_file_path

def chunked_upload_with_progress(session, url, temp_file_path, headers, total_size, 
                                chunk_size=CHUNK_SIZE, timeout=UPLOAD_TIMEOUT):
    """Upload extremely large astronomical data in chunks with a progress bar."""
    
    try:
        with tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024,
                 desc="Uploading astronomical data", bar_format='{desc}: {percentage:3.1f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]') as pbar:
            
            # Add Content-Length header
            headers['Content-Length'] = str(total_size)
            
            # For chunked uploads, we'll use a streaming approach that doesn't load entire file in memory
            with open(temp_file_path, 'rb') as f:
                def iter_chunks():
                    bytes_read = 0
                    while True:
                        chunk = f.read(chunk_size)
                        if not chunk:
                            break
                        bytes_read += len(chunk)
                        pbar.update(len(chunk))
                        yield chunk
                
                response = session.put(
                    url,
                    data=iter_chunks(),
                    headers=headers,
                    timeout=timeout
                )
                
                return response
    except Exception as e:
        debug_print(f"Chunked upload error: {str(e)}")
        raise

def upload_large_file(data_to_upload, metadata=None):
    """
    Handle upload of extremely large astronomical data files (up to 50GB)

    Args:
        data_to_upload: The astronomical data to upload (array, dataframe, fits, etc.)
        metadata: Optional metadata to include with the upload

    Returns:
        dict: Information about the uploaded data
    """
    # Get the API key
    from ..auth import get_api_key
    api_key = get_api_key()
    
    # Set up the request
    print("Preparing astronomical data for upload...")
    temp_files = []  # Track temp files for cleanup
    
    try:
        # Create a robust session with optimized retry logic for astronomical data
        session = create_robust_session()
        
        # First, get the presigned URL for upload
        headers = {
            'x-api-key': api_key
        }

        response = session.post(
            'https://lbmoem9mdg.execute-api.us-west-1.amazonaws.com/prod/nerd-mega-compute/data/large',
            headers=headers,
            timeout=CONNECTION_TIMEOUT
        )

        if response.status_code != 200:
            error_msg = f"Failed to get presigned URL for large astronomical data upload: {response.text}"
            print(f"❌ {error_msg}")
            raise Exception(error_msg)

        upload_info = response.json()
        upload_url = upload_info['presignedUrl']

        # Convert data to optimized binary format
        try:
            print(f"Optimizing astronomical data for upload...")
            binary_data, storage_format = optimize_data_for_upload(data_to_upload)
            
            # Get data size for progress reporting
            data_size = len(binary_data)
            data_size_mb = data_size / (1024 * 1024)
            data_size_gb = data_size_mb / 1024
            
            # Show appropriate size units
            if data_size_gb >= 1:
                print(f"Preparing to upload {data_size_gb:.2f}GB of astronomical data...")
            else:
                print(f"Preparing to upload {data_size_mb:.2f}MB of astronomical data...")
            
            # Set content type based on storage format
            content_type = 'application/python-pickle' if storage_format == 'pickle' else 'application/octet-stream'
            if storage_format == 'numpy':
                content_type = 'application/numpy-array'
                
            upload_headers = {
                'Content-Type': content_type
            }
            
            # For very large astronomical datasets, use temp file to reduce memory pressure
            print("Moving data to temporary storage to optimize memory usage...")
            temp_file_path = get_memory_optimized_temp_file(binary_data)
            temp_files.append(temp_file_path)
            
            # Free up memory immediately after creating temp file
            del binary_data
            
            # Determine upload strategy based on size
            success = False
            max_attempts = MAX_RETRIES
            
            for attempt in range(max_attempts):
                try:
                    if attempt > 0:
                        print(f"\nRetry attempt {attempt+1}/{max_attempts} for astronomical data upload...")
                    
                    # Use chunked upload for all astronomical data (typically large)
                    upload_response = chunked_upload_with_progress(
                        session, 
                        upload_url, 
                        temp_file_path, 
                        upload_headers,
                        total_size=data_size,
                        chunk_size=CHUNK_SIZE,
                        timeout=UPLOAD_TIMEOUT
                    )
                    
                    # Check response
                    if upload_response.status_code in [200, 201, 204]:
                        success = True
                        print(f"\n✅ Astronomical data upload completed successfully!")
                        break
                    else:
                        print(f"\n⚠️ Upload failed with status code: {upload_response.status_code}")
                        print(f"Response: {upload_response.text[:500]}")  # Truncate long responses
                        
                        # Wait before retrying with exponential backoff
                        if attempt < max_attempts - 1:
                            retry_wait = min(300, RETRY_BACKOFF ** (attempt + 2))  # Cap at 5 minutes
                            print(f"Waiting {retry_wait:.1f} seconds before retrying...")
                            time.sleep(retry_wait)
                            
                except Exception as e:
                    print(f"\n⚠️ Upload attempt {attempt+1} failed: {str(e)}")
                    debug_print(traceback.format_exc())
                    
                    # Wait before retrying with longer backoff for network issues
                    if attempt < max_attempts - 1:
                        retry_wait = min(300, 10 * (attempt + 1))  # More aggressive backoff, cap at 5 minutes
                        print(f"Waiting {retry_wait:.1f} seconds before retrying...")
                        time.sleep(retry_wait)
            
            # If all attempts failed, raise exception
            if not success:
                error_msg = "Failed to upload large astronomical data after multiple attempts"
                print(f"\n❌ {error_msg}")
                raise Exception(error_msg)

            # Report success with appropriate size units
            if data_size_gb >= 1:
                print(f"✅ Astronomical data uploaded successfully! Size: {data_size_gb:.2f}GB")
            else:
                print(f"✅ Astronomical data uploaded successfully! Size: {data_size_mb:.2f}MB")
                
            print(f"📋 Data ID: {upload_info['dataId']}")
            print(f"🔗 S3 URI: {upload_info['s3Uri']}")

            # Return a response in the standard format
            return {
                'dataId': upload_info['dataId'],
                's3Uri': upload_info['s3Uri'],
                'storageFormat': storage_format,
                'sizeMB': f"{data_size_mb:.2f}",
                'contentType': content_type
            }
            
        except Exception as e:
            error_msg = f"Failed to process astronomical data: {e}"
            debug_print(traceback.format_exc())
            print(f"❌ {error_msg}")
            raise Exception(error_msg)

    except Exception as e:
        print(f"❌ Error during large astronomical data upload: {e}")
        debug_print(traceback.format_exc())
        # Re-raise the exception with more context
        raise Exception(f"Large astronomical data upload failed: {e}") from e
    finally:
        # Clean up all temporary files
        for temp_file in temp_files:
            try:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
                    debug_print(f"Cleaned up temporary file: {temp_file}")
            except Exception as e:
                debug_print(f"Failed to clean up temporary file {temp_file}: {e}")