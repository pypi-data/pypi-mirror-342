import json
import base64
import pickle
import zlib
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
    if storage_format == "json":
        # Already parsed as JSON by requests.json()
        return data
    elif storage_format in ["binary", "pickle"]:
        if isinstance(data, str) and is_likely_base64(data):
            try:
                # 1. Decode from base64
                binary_data = base64.b64decode(data)
                
                # 2. Try decompress (might be compressed)
                try:
                    decompressed = zlib.decompress(binary_data)
                    # 3. Unpickle to get original object (use protocol 4 for compatibility)
                    return pickle.loads(decompressed)
                except zlib.error:
                    # If decompression fails, try direct unpickling (might not be compressed)
                    debug_print("Decompression failed, trying direct unpickling")
                    return pickle.loads(binary_data)
                    
            except Exception as e:
                debug_print(f"Error decoding and decompressing data: {e}")
                # Try different pickle protocols if initial attempt fails
                try:
                    binary_data = base64.b64decode(data)
                    for protocol in [4, 5, 3]:
                        try:
                            debug_print(f"Trying pickle protocol {protocol}")
                            return pickle.loads(binary_data, fix_imports=True, encoding='bytes')
                        except:
                            pass
                except:
                    pass
                
                # Fallback to original approach
                return data
                
        # Handle bytes data directly
        elif isinstance(data, bytes):
            try:
                # Try to decompress first, then unpickle
                try:
                    decompressed = zlib.decompress(data)
                    return pickle.loads(decompressed)
                except zlib.error:
                    # If decompression fails, try direct unpickling
                    debug_print("Direct decompression failed, trying direct unpickling")
                    return pickle.loads(data)
            except Exception as e:
                debug_print(f"Error unpickling binary data: {e}")
                return data
                
        # Already binary data
        return data
    else:
        # Unknown format, return as-is
        return data