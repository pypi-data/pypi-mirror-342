import json
import base64
import pickle
import zlib
import time
from ...utils import debug_print

def is_likely_base64(data):
    """
    Check if a string is likely base64 encoded

    Args:
        data: String to check

    Returns:
        bool: True if the string appears to be base64 encoded
    """
    if not isinstance(data, str):
        return False

    # Check if string only contains base64 valid characters
    try:
        if not all(c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=' for c in data):
            return False

        # Try to decode the base64 string
        decoded = base64.b64decode(data)
        return True
    except Exception:
        return False

def parse_fetched_data(data, storage_format):
    """
    Parse data fetched from cloud storage based on storage format

    Args:
        data: The fetched data
        storage_format: Format of the stored data (json, binary, pickle)

    Returns:
        The parsed data object
    """
    print(f"[PARSING_DEBUG] parse_fetched_data called with format: {storage_format}, data type: {type(data).__name__}")
    
    if storage_format == "json":
        print("[PARSING_DEBUG] Processing as JSON format")
        # Already parsed as JSON by requests.json()
        if isinstance(data, dict) or isinstance(data, list):
            print(f"[PARSING_DEBUG] Data is already parsed as JSON: {type(data).__name__}")
            return data
        elif isinstance(data, str):
            try:
                print("[PARSING_DEBUG] Attempting to parse JSON string")
                parsed = json.loads(data)
                print(f"[PARSING_DEBUG] Successfully parsed JSON string into {type(parsed).__name__}")
                return parsed
            except Exception as e:
                print(f"[PARSING_DEBUG] Failed to parse as JSON string: {e}")
                return data
        else:
            print(f"[PARSING_DEBUG] Unexpected data type for JSON format: {type(data).__name__}")
            return data
            
    elif storage_format in ["binary", "pickle"]:
        print("[PARSING_DEBUG] Processing as binary/pickle format")
        
        if isinstance(data, str) and is_likely_base64(data):
            print("[PARSING_DEBUG] Data appears to be base64 encoded")
            try:
                # Approach 1: Standard compressed pickle format
                print("[PARSING_DEBUG] Trying: base64 decode + zlib decompress + pickle load")
                start_time = time.time()
                # 1. Decode from base64
                binary_data = base64.b64decode(data)
                print(f"[PARSING_DEBUG] Base64 decoded size: {len(binary_data) / (1024 * 1024):.2f} MB")
                
                # 2. Decompress the data
                decompressed = zlib.decompress(binary_data)
                print(f"[PARSING_DEBUG] Decompressed size: {len(decompressed) / (1024 * 1024):.2f} MB")
                
                # 3. Unpickle to get original object
                result = pickle.loads(decompressed)
                print(f"[PARSING_DEBUG] Successfully unpickled in {time.time() - start_time:.2f}s, result type: {type(result).__name__}")
                
                # Print information about the result
                if hasattr(result, 'shape'):
                    print(f"[PARSING_DEBUG] Result has shape: {result.shape}")
                elif isinstance(result, dict):
                    keys = list(result.keys())[:20] if result else []
                    print(f"[PARSING_DEBUG] Result is dict with keys: {keys}")
                elif isinstance(result, list):
                    print(f"[PARSING_DEBUG] Result is list with {len(result)} items")
                    if result and len(result) > 0:
                        print(f"[PARSING_DEBUG] First item type: {type(result[0]).__name__}")
                
                return result
            except Exception as e:
                print(f"[PARSING_DEBUG] Standard approach failed: {e}")
                
                # Try alternate approaches
                try:
                    # Approach 2: Just decode base64 and try to unpickle
                    print("[PARSING_DEBUG] Trying: base64 decode + pickle load")
                    binary_data = base64.b64decode(data)
                    result = pickle.loads(binary_data)
                    print(f"[PARSING_DEBUG] Successfully unpickled with alternate approach, result type: {type(result).__name__}")
                    return result
                except Exception as e:
                    print(f"[PARSING_DEBUG] Alternate approach failed: {e}")
                    
                print("[PARSING_DEBUG] Returning original data after all approaches failed")
                return data
        elif isinstance(data, bytes):
            print("[PARSING_DEBUG] Data is already in bytes format")
            try:
                # 1. Try direct unpickling
                print("[PARSING_DEBUG] Trying direct pickle load")
                start_time = time.time()
                result = pickle.loads(data)
                print(f"[PARSING_DEBUG] Successfully unpickled in {time.time() - start_time:.2f}s, result type: {type(result).__name__}")
                return result
            except Exception as e:
                print(f"[PARSING_DEBUG] Direct unpickling failed: {e}")
                
                # 2. Try decompress + unpickle
                try:
                    print("[PARSING_DEBUG] Trying zlib decompress + pickle load")
                    start_time = time.time()
                    decompressed = zlib.decompress(data)
                    print(f"[PARSING_DEBUG] Decompressed size: {len(decompressed) / (1024 * 1024):.2f} MB")
                    result = pickle.loads(decompressed)
                    print(f"[PARSING_DEBUG] Successfully decompressed and unpickled in {time.time() - start_time:.2f}s, result type: {type(result).__name__}")
                    return result
                except Exception as e:
                    print(f"[PARSING_DEBUG] Decompress + unpickle failed: {e}")
                
                # Return original bytes if all approaches fail
                print("[PARSING_DEBUG] All binary parsing approaches failed, returning original bytes")
                return data
        else:
            print(f"[PARSING_DEBUG] Unexpected data type for binary/pickle format: {type(data).__name__}")
            return data
    else:
        # Unknown format, return as-is
        print(f"[PARSING_DEBUG] Unknown storage format: {storage_format}, returning as-is")
        return data