# Automatically resolve references
def resolve_references(obj):
    if isinstance(obj, dict) and "__nerd_data_reference" in obj:
        # This is a reference to cloud storage
        data_id = obj["__nerd_data_reference"]
        s3_uri = obj.get("__nerd_s3_uri", "")
        print(f"Auto-resolving data reference: {data_id}")

        # This assumes the cloud has access to this data
        import boto3
        import io
        import pickle
        import zlib
        import numpy as np
        from pandas import DataFrame
        
        # Get the bucket and key from S3 URI
        if s3_uri.startswith("s3://"):
            parts = s3_uri[5:].split("/", 1)
            if len(parts) == 2:
                bucket = parts[0]
                key = parts[1]

                # Download the data
                s3 = boto3.client('s3')
                try:
                    buffer = io.BytesIO()
                    s3.download_fileobj(bucket, key, buffer)
                    buffer.seek(0)
                    raw_data = buffer.read()
                    print(f"Successfully retrieved data: {len(raw_data) / (1024 * 1024):.2f} MB")
                    
                    try:
                        # First try to decompress then unpickle - use protocol 4 for compatibility
                        decompressed_data = zlib.decompress(raw_data)
                        unpickled_data = pickle.loads(decompressed_data)
                        print(f"Successfully unpickled data of type: {type(unpickled_data).__name__}")
                        return unpickled_data
                        
                    except Exception as e:
                        print(f"Error processing data: {e}")
                        # Try alternate approaches for backwards compatibility
                        try:
                            # Try just unpickling directly
                            direct_unpickled = pickle.loads(raw_data)
                            print(f"Successfully unpickled raw data of type: {type(direct_unpickled).__name__}")
                            return direct_unpickled
                        except Exception as e2:
                            print(f"Error unpickling raw data: {e2}")
                            return raw_data
                    
                except Exception as e:
                    print(f"Error retrieving data: {e}")
                    # Fall through to return the original reference

    elif isinstance(obj, list):
        return [resolve_references(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: resolve_references(v) for k, v in obj.items()}
    return obj

# Automatically resolve references before calling the function
def auto_reference_wrapper(func, args, kwargs):
    resolved_args = [resolve_references(arg) for arg in args]
    resolved_kwargs = {k: resolve_references(v) for k, v in kwargs.items()}
    return func(*resolved_args, **resolved_kwargs)