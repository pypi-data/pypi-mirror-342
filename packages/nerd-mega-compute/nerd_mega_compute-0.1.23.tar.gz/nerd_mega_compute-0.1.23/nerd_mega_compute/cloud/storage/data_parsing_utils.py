import base64
import cloudpickle
from ...utils import debug_print

def serialize_data(data):
    """
    Simple, consistent serialization approach for all data types:
    1. Use cloudpickle to serialize (preserves object structure and methods)
    2. Base64 encode the result for safe transport

    Args:
        data: Any Python object to serialize

    Returns:
        tuple: (serialized_data, metadata_dict)
    """
    try:
        # Serialize with cloudpickle
        debug_print(f"Serializing object of type: {type(data).__name__}")
        pickled_data = cloudpickle.dumps(data)

        # Base64 encode for safe transport
        serialized = base64.b64encode(pickled_data).decode('utf-8')

        # Keep track of the original type
        metadata = {
            'format': 'cloudpickle-base64',
            'original_type': type(data).__name__
        }

        debug_print(f"Successfully serialized {len(serialized)/1024:.2f} KB data")
        return serialized, metadata
    except Exception as e:
        debug_print(f"Error in serialize_data: {e}")
        # Fallback to string representation
        return str(data), {'format': 'string', 'error': str(e)}

def deserialize_data(data, metadata=None):
    """
    Simple, consistent deserialization approach:
    1. Decode from base64
    2. Use cloudpickle to deserialize

    Args:
        data: Serialized data (bytes or string)
        metadata: Optional metadata about the data format

    Returns:
        The deserialized Python object
    """
    if not data:
        return None

    # If we have metadata and it's our format, use our approach
    if metadata and metadata.get('format') == 'cloudpickle-base64':
        try:
            debug_print(f"Deserializing data with format: {metadata.get('format')}")

            # If data is a string, decode from base64
            if isinstance(data, str):
                binary_data = base64.b64decode(data)
            # If data is already bytes, use directly
            elif isinstance(data, bytes):
                binary_data = data
            else:
                debug_print(f"Unexpected data type: {type(data).__name__}")
                return data

            # Deserialize with cloudpickle
            result = cloudpickle.loads(binary_data)
            debug_print(f"Successfully deserialized to: {type(result).__name__}")
            return result
        except Exception as e:
            debug_print(f"Error in deserialize_data: {e}")
            return data

    # If no metadata or unknown format, try various approaches
    try:
        # For bytes data
        if isinstance(data, bytes):
            try:
                return cloudpickle.loads(data)
            except Exception as e:
                debug_print(f"Failed to deserialize bytes: {e}")

        # For string data that might be base64
        if isinstance(data, str):
            try:
                binary_data = base64.b64decode(data)
                return cloudpickle.loads(binary_data)
            except Exception as e:
                debug_print(f"Failed to deserialize base64 string: {e}")

        # Return as is if nothing worked
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