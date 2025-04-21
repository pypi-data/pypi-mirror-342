import json
import base64
import pickle
import zlib
from ...utils import debug_print

def serialize_data(data):
    """
    Serialize data for transport to cloud storage using a consistent approach:
    1. Pickle the data (maintains type information)
    2. Compress the pickled data with zlib
    3. Encode as base64 for safe transport

    Args:
        data: Any Python object to serialize

    Returns:
        tuple: (serialized_data, metadata_dict)
    """
    try:
        # 1. Pickle the data to preserve exact type information
        pickled_data = pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL)

        # 2. Compress the pickled data
        compressed_data = zlib.compress(pickled_data)

        # 3. Base64 encode for safe transport
        encoded_data = base64.b64encode(compressed_data).decode('utf-8')

        # Return serialized data and metadata
        metadata = {
            'format': 'pickle-zlib-base64',
            'original_type': type(data).__name__
        }

        return encoded_data, metadata
    except Exception as e:
        debug_print(f"Error in serialize_data: {e}")
        # Fallback to string representation if all else fails
        return str(data), {'format': 'string', 'error': str(e)}

def deserialize_data(data, metadata=None):
    """
    Deserialize data from cloud storage using a consistent approach:
    1. Decode from base64
    2. Decompress the data
    3. Unpickle to get original object

    Args:
        data: Serialized data string
        metadata: Optional metadata about the data format

    Returns:
        The deserialized Python object
    """
    if not data:
        return None

    # Handle the standardized format: pickle-zlib-base64
    if metadata and metadata.get('format') == 'pickle-zlib-base64':
        try:
            # 1. Decode from base64
            binary_data = base64.b64decode(data)
            # 2. Decompress
            decompressed = zlib.decompress(binary_data)
            # 3. Unpickle
            return pickle.loads(decompressed)
        except Exception as e:
            debug_print(f"Error deserializing data: {e}")
            return data

    # Legacy format handling
    try:
        # Try to decode as base64 and unpickle
        if isinstance(data, str) and all(c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=' for c in data):
            try:
                # Try base64 decode + zlib decompress + unpickle
                binary_data = base64.b64decode(data)
                try:
                    # Try with decompression first
                    decompressed = zlib.decompress(binary_data)
                    return pickle.loads(decompressed)
                except:
                    # Try without decompression
                    return pickle.loads(binary_data)
            except:
                pass

        # If it's a string, try JSON decoding
        if isinstance(data, str):
            try:
                return json.loads(data)
            except:
                pass

        # Return as-is if nothing worked
        return data
    except Exception as e:
        debug_print(f"Error in deserialize_data fallback: {e}")
        return data

def parse_fetched_data(data, storage_format):
    """
    Parse data fetched from cloud storage based on storage format

    Args:
        data: The fetched data
        storage_format: Format of the stored data

    Returns:
        The parsed data object
    """
    metadata = {'format': storage_format}
    return deserialize_data(data, metadata)