# Automatically resolve references
def resolve_references(obj):
    if isinstance(obj, dict) and "__nerd_data_reference" in obj:
        # This is a reference to cloud storage
        data_id = obj["__nerd_data_reference"]
        s3_uri = obj.get("__nerd_s3_uri", "")
        print(f"Auto-resolving data reference: {data_id}")

        # This assumes the cloud has access to this data
        from boto3 import client
        import io
        import pickle
        import base64
        import zlib

        # Get the bucket and key from S3 URI
        if s3_uri.startswith("s3://"):
            parts = s3_uri[5:].split("/", 1)
            if len(parts) == 2:
                bucket = parts[0]
                key = parts[1]

                # Download the data
                s3 = client('s3')
                try:
                    buffer = io.BytesIO()
                    s3.download_fileobj(bucket, key, buffer)
                    buffer.seek(0)
                    data = buffer.read()
                    print(f"Successfully retrieved data: {len(data) / (1024 * 1024):.2f} MB")
                    
                    # Try to deserialize data if it's compressed or pickled
                    try:
                        # First try to decompress with zlib
                        decompressed = zlib.decompress(data)
                        # Then try to unpickle
                        unpickled = pickle.loads(decompressed)
                        print("Data was successfully decompressed and unpickled")
                        return unpickled
                    except Exception as e:
                        print(f"Data was not compressed/pickled format: {e}")
                        # Return raw data if decompression/unpickling fails
                        return data
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