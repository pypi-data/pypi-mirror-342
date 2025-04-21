import json
import base64
import pickle
import zlib
import cloudpickle
from ...utils import debug_print

def serialize_data(data):
    """
    Serialize data for transport to cloud storage using cloudpickle for maximum compatibility.
    
    Args:
        data: Any Python object to serialize
        
    Returns:
        tuple: (serialized_data, metadata_dict)
    """
    try:
        # Use cloudpickle instead of pickle for better handling of complex objects
        # This is critical for classes like DataFrames, ML models, and special arrays
        pickled_data = cloudpickle.dumps(data)
        
        # Add a special marker to identify our format
        # This helps us distinguish this from other serialization methods
        metadata = {
            'format': 'cloudpickle-binary',
            'original_type': type(data).__name__
        }
        
        # Return the data as binary content directly - no base64 or compression
        # Let S3 handle this as a raw binary object
        return pickled_data, metadata
    except Exception as e:
        debug_print(f"Error in serialize_data: {e}")
        # Fallback to string representation if all else fails
        return str(data), {'format': 'string', 'error': str(e)}

def deserialize_data(data, metadata=None):
    """
    Deserialize data from cloud storage.
    
    Args:
        data: Serialized data (bytes or string)
        metadata: Optional metadata about the data format
        
    Returns:
        The deserialized Python object
    """
    if not data:
        return None
    
    # Handle our special format: cloudpickle-binary
    if metadata and metadata.get('format') == 'cloudpickle-binary':
        try:
            # The data should already be binary
            if isinstance(data, bytes):
                return cloudpickle.loads(data)
            elif isinstance(data, str):
                # If for some reason it's a string, try to convert to bytes
                try:
                    return cloudpickle.loads(base64.b64decode(data))
                except:
                    debug_print("Failed to decode as base64, trying direct loading")
                    return cloudpickle.loads(data.encode('latin1'))
            else:
                debug_print(f"Unexpected data type in deserialize_data: {type(data)}")
                return data
        except Exception as e:
            debug_print(f"Error deserializing cloudpickle data: {e}")
            return data
    
    # For other formats, handle appropriately
    try:
        # If it's already bytes, try direct unpickling
        if isinstance(data, bytes):
            try:
                # Try cloudpickle first
                return cloudpickle.loads(data)
            except:
                # Fall back to regular pickle
                try:
                    return pickle.loads(data)
                except:
                    pass
                    
            # Try with decompression if direct unpickling fails
            try:
                decompressed = zlib.decompress(data)
                try:
                    return cloudpickle.loads(decompressed)
                except:
                    return pickle.loads(decompressed)
            except:
                pass
        
        # If it's a string, try base64 decoding first
        if isinstance(data, str):
            # Check if it might be a base64 string
            if all(c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=' for c in data):
                try:
                    binary_data = base64.b64decode(data)
                    
                    # Try direct unpickling
                    try:
                        return cloudpickle.loads(binary_data)
                    except:
                        try:
                            return pickle.loads(binary_data)
                        except:
                            pass
                    
                    # Try with decompression
                    try:
                        decompressed = zlib.decompress(binary_data)
                        try:
                            return cloudpickle.loads(decompressed)
                        except:
                            return pickle.loads(decompressed)
                    except:
                        pass
                except:
                    pass
            
            # Try JSON decoding
            try:
                return json.loads(data)
            except:
                pass
                
        # Return as-is if nothing else worked
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