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
                # 2. Decompress the data
                decompressed = zlib.decompress(binary_data)
                # 3. Unpickle to get original object
                return pickle.loads(decompressed)
            except Exception as e:
                debug_print(f"Error decoding and decompressing data: {e}")
                # Fallback to original approach
                return data
        # Already binary data
        return data
    else:
        # Unknown format, return as-is
        return data