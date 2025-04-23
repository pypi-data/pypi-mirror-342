from ..utils import debug_print
import pickle
import base64
import zlib
import requests
import traceback
import time

def fetch_nerd_data_reference(data_ref):
    """
    Retrieve data from a cloud storage reference.

    This function is intended to be used inside cloud compute functions to retrieve
    large binary data that was automatically uploaded to cloud storage.

    Args:
        data_ref (dict): A data reference object containing __nerd_data_reference key

    Returns:
        The retrieved data from cloud storage
    """
    print(f"[STORAGE_DEBUG] fetch_nerd_data_reference called at {time.time()}")
    
    # Check if this is a valid data reference
    if not isinstance(data_ref, dict):
        print(f"[STORAGE_DEBUG] Not a dictionary reference object: {type(data_ref)}")
        return data_ref

    # Check for our special reference format
    if "__nerd_data_reference" in data_ref:
        data_id = data_ref["__nerd_data_reference"]
        s3_uri = data_ref.get("__nerd_s3_uri", "")
        size_mb = data_ref.get("__nerd_size_mb", "unknown")
        print(f"[STORAGE_DEBUG] Fetching data from cloud storage reference: {data_id}, S3 URI: {s3_uri}, Size: {size_mb}MB")

        # First try direct S3 access if URI is provided
        if s3_uri and s3_uri.startswith("s3://"):
            try:
                print(f"[STORAGE_DEBUG] Attempting direct S3 access for URI: {s3_uri}")
                from boto3 import client
                import io
                
                # Parse bucket and key from S3 URI
                parts = s3_uri[5:].split("/", 1)
                if len(parts) == 2:
                    bucket = parts[0]
                    key = parts[1]
                    
                    print(f"[STORAGE_DEBUG] Fetching directly from S3: bucket={bucket}, key={key}")
                    s3 = client('s3')
                    
                    # Get object metadata first
                    try:
                        head_response = s3.head_object(Bucket=bucket, Key=key)
                        content_type = head_response.get('ContentType', 'application/octet-stream')
                        content_length = head_response.get('ContentLength', 0)
                        print(f"[STORAGE_DEBUG] S3 object metadata: Content-Type={content_type}, Size={content_length / (1024 * 1024):.2f}MB")
                    except Exception as e:
                        print(f"[STORAGE_DEBUG] Error getting S3 metadata: {e}")
                    
                    # Download as stream to memory
                    buffer = io.BytesIO()
                    start_time = time.time()
                    s3.download_fileobj(bucket, key, buffer)
                    download_time = time.time() - start_time
                    buffer.seek(0)
                    data = buffer.read()
                    
                    data_size_mb = len(data) / (1024 * 1024)
                    print(f"[STORAGE_DEBUG] Successfully downloaded {data_size_mb:.2f}MB from S3 in {download_time:.2f} seconds")
                    print(f"[STORAGE_DEBUG] First 50 bytes (hex): {data[:50].hex()}")
                    print(f"[STORAGE_DEBUG] Last 50 bytes (hex): {data[-50:].hex()}")
                    
                    # Try multiple deserialization approaches
                    deserialization_start = time.time()
                    try:
                        # First try if it's compressed and pickled (our standard format)
                        try:
                            print("[STORAGE_DEBUG] Attempting zlib decompression + pickle")
                            decompressed = zlib.decompress(data)
                            decompressed_size_mb = len(decompressed) / (1024 * 1024)
                            print(f"[STORAGE_DEBUG] Decompression successful, size: {decompressed_size_mb:.2f}MB")
                            pickle_start = time.time()
                            result = pickle.loads(decompressed)
                            pickle_time = time.time() - pickle_start
                            print(f"[STORAGE_DEBUG] Successfully unpickled in {pickle_time:.2f}s, result type: {type(result).__name__}")
                            
                            # Print additional info about the result object
                            if hasattr(result, '__dict__'):
                                print(f"[STORAGE_DEBUG] Object attributes: {dir(result)[:20]}")
                            elif isinstance(result, dict):
                                print(f"[STORAGE_DEBUG] Dictionary keys: {list(result.keys())[:20] if len(result) > 0 else 'empty'}")
                            elif hasattr(result, 'shape'):
                                print(f"[STORAGE_DEBUG] Array shape: {result.shape}")
                                
                            print(f"[STORAGE_DEBUG] Total deserialization time: {time.time() - deserialization_start:.2f}s")
                            return result
                        except Exception as e:
                            print(f"[STORAGE_DEBUG] zlib+pickle approach failed: {str(e)}")
                        
                        # Try if it's directly pickled
                        try:
                            print("[STORAGE_DEBUG] Attempting direct pickle deserialization")
                            pickle_start = time.time()
                            result = pickle.loads(data)
                            pickle_time = time.time() - pickle_start
                            print(f"[STORAGE_DEBUG] Successfully unpickled in {pickle_time:.2f}s, result type: {type(result).__name__}")
                            print(f"[STORAGE_DEBUG] Total deserialization time: {time.time() - deserialization_start:.2f}s")
                            return result
                        except Exception as e:
                            print(f"[STORAGE_DEBUG] Direct pickle approach failed: {str(e)}")
                        
                        # Try if it's base64 encoded
                        if len(data) > 0 and all(c in b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=' for c in data[:100]):
                            try:
                                print("[STORAGE_DEBUG] Data appears to be base64 encoded, attempting decode")
                                decoded = base64.b64decode(data)
                                decoded_size_mb = len(decoded) / (1024 * 1024)
                                print(f"[STORAGE_DEBUG] Base64 decoding successful, size: {decoded_size_mb:.2f}MB")
                                
                                # Try uncompressing and unpickling
                                try:
                                    print("[STORAGE_DEBUG] Attempting zlib decompression of decoded data")
                                    decompressed = zlib.decompress(decoded)
                                    decompressed_size_mb = len(decompressed) / (1024 * 1024)
                                    print(f"[STORAGE_DEBUG] Decompression successful, size: {decompressed_size_mb:.2f}MB")
                                    
                                    pickle_start = time.time()
                                    result = pickle.loads(decompressed)
                                    pickle_time = time.time() - pickle_start
                                    print(f"[STORAGE_DEBUG] Successfully unpickled in {pickle_time:.2f}s, result type: {type(result).__name__}")
                                    print(f"[STORAGE_DEBUG] Total deserialization time: {time.time() - deserialization_start:.2f}s")
                                    return result
                                except Exception as e:
                                    print(f"[STORAGE_DEBUG] zlib+pickle of decoded data failed: {str(e)}")
                                
                                # Try direct unpickling of decoded data
                                try:
                                    print("[STORAGE_DEBUG] Attempting direct pickle of decoded data")
                                    pickle_start = time.time()
                                    result = pickle.loads(decoded)
                                    pickle_time = time.time() - pickle_start
                                    print(f"[STORAGE_DEBUG] Successfully unpickled in {pickle_time:.2f}s, result type: {type(result).__name__}")
                                    print(f"[STORAGE_DEBUG] Total deserialization time: {time.time() - deserialization_start:.2f}s")
                                    return result
                                except Exception as e:
                                    print(f"[STORAGE_DEBUG] Direct pickle of decoded data failed: {str(e)}")
                            except Exception as e:
                                print(f"[STORAGE_DEBUG] Base64 decoding failed: {str(e)}")
                        
                        # Return the raw data if all deserialization attempts failed
                        print("[STORAGE_DEBUG] All deserialization approaches failed, returning raw binary data")
                        return data
                    except Exception as e:
                        print(f"[STORAGE_DEBUG] Error in deserializing data: {str(e)}")
                        traceback.print_exc()
                        return data
            except Exception as e:
                print(f"[STORAGE_DEBUG] Error in S3 access: {str(e)}")
                traceback.print_exc()
                # Fall through to the API method if S3 fails

        # Fallback to standard API fetch
        try:
            print(f"[STORAGE_DEBUG] Attempting API fetch for data ID: {data_id}")
            # Import locally to avoid circular imports
            from .storage import fetch_nerd_cloud_storage
            api_start = time.time()
            fetched_data = fetch_nerd_cloud_storage(data_id)
            api_time = time.time() - api_start
            print(f"[STORAGE_DEBUG] API fetch completed in {api_time:.2f}s, result type: {type(fetched_data).__name__}")
            
            # If we got binary data, try to deserialize it
            if isinstance(fetched_data, bytes):
                print(f"[STORAGE_DEBUG] API returned binary data, size: {len(fetched_data) / (1024 * 1024):.2f}MB")
                print(f"[STORAGE_DEBUG] First 50 bytes (hex): {fetched_data[:50].hex()}")
                print(f"[STORAGE_DEBUG] Last 50 bytes (hex): {fetched_data[-50:].hex()}")
                
                deserialization_start = time.time()
                try:
                    # Try multiple deserialization approaches again
                    try:
                        print("[STORAGE_DEBUG] Attempting zlib decompression + pickle of API data")
                        decompressed = zlib.decompress(fetched_data)
                        decompressed_size_mb = len(decompressed) / (1024 * 1024)
                        print(f"[STORAGE_DEBUG] Decompression successful, size: {decompressed_size_mb:.2f}MB")
                        
                        pickle_start = time.time()
                        result = pickle.loads(decompressed)
                        pickle_time = time.time() - pickle_start
                        print(f"[STORAGE_DEBUG] Successfully unpickled in {pickle_time:.2f}s, result type: {type(result).__name__}")
                        print(f"[STORAGE_DEBUG] Total API deserialization time: {time.time() - deserialization_start:.2f}s")
                        return result
                    except Exception as e:
                        print(f"[STORAGE_DEBUG] API data zlib+pickle approach failed: {str(e)}")
                    
                    try:
                        print("[STORAGE_DEBUG] Attempting direct pickle of API data")
                        pickle_start = time.time()
                        result = pickle.loads(fetched_data)
                        pickle_time = time.time() - pickle_start
                        print(f"[STORAGE_DEBUG] Successfully unpickled in {pickle_time:.2f}s, result type: {type(result).__name__}")
                        print(f"[STORAGE_DEBUG] Total API deserialization time: {time.time() - deserialization_start:.2f}s")
                        return result
                    except Exception as e:
                        print(f"[STORAGE_DEBUG] API data direct pickle approach failed: {str(e)}")
                    
                    # Return binary data as is
                    print("[STORAGE_DEBUG] All API data deserialization approaches failed, returning raw binary")
                    return fetched_data
                except Exception as e:
                    print(f"[STORAGE_DEBUG] Error deserializing API data: {str(e)}")
                    traceback.print_exc()
                    return fetched_data
            
            print(f"[STORAGE_DEBUG] Returning non-binary API result: {type(fetched_data).__name__}")
            return fetched_data
        except Exception as e:
            print(f"[STORAGE_DEBUG] API fetch failed: {str(e)}")
            traceback.print_exc()
            return data_ref  # Return the reference if all fetch methods fail

    # Handle other reference formats
    elif isinstance(data_ref, dict) and "type" in data_ref and data_ref["type"] == "bytes_reference":
        # This is the format from serialize_with_chunking
        print("[STORAGE_DEBUG] Found bytes_reference format")
        ref_data = data_ref.get("value", {})
        if isinstance(ref_data, dict) and "data_reference" in ref_data:
            data_id = ref_data["data_reference"]
            s3_uri = ref_data.get("s3Uri", "")
            size_mb = ref_data.get("sizeMB", "")
            print(f"[STORAGE_DEBUG] Processing bytes_reference with ID: {data_id}, URI: {s3_uri}, Size: {size_mb}")
            # Convert to our standard format and recursively handle it
            std_ref = {
                "__nerd_data_reference": data_id,
                "__nerd_s3_uri": s3_uri,
                "__nerd_size_mb": size_mb
            }
            return fetch_nerd_data_reference(std_ref)
    
    # If this is not our reference format, return as-is
    print(f"[STORAGE_DEBUG] Not recognized as a data reference, returning as-is: {type(data_ref).__name__}")
    return data_ref