import pickle
import base64
import zlib
import json
import time
import os
import traceback
import sys
import cloudpickle

# This function unpacks the data we sent
def deserialize_arg(arg_data):
    if isinstance(arg_data, dict):
        if 'type' in arg_data:
            if arg_data['type'] == 'data' or arg_data['type'] == 'cloudpickle':
                try:
                    # 1. Decode from base64
                    binary_data = base64.b64decode(arg_data['value'])
                    # 2. Decompress if needed
                    if arg_data['type'] == 'data':
                        binary_data = zlib.decompress(binary_data)
                    # 3. Unpickle using cloudpickle
                    return cloudpickle.loads(binary_data)
                except Exception as e:
                    print(f"Error deserializing with cloudpickle: {e}")
                    return arg_data['value']
            elif arg_data['type'] == 'bytes_reference':
                # Handle S3 references for large binary data
                try:
                    import boto3
                    s3_uri = arg_data['value'].get('s3Uri', '')
                    if s3_uri.startswith('s3://'):
                        parts = s3_uri.replace('s3://', '').split('/', 1)
                        if len(parts) == 2:
                            bucket = parts[0]
                            key = parts[1]
                            print(f"Downloading data from {s3_uri}")
                            s3 = boto3.client('s3')
                            response = s3.get_object(Bucket=bucket, Key=key)
                            return response['Body'].read()
                    return f"Could not load S3 reference: {s3_uri}"
                except Exception as e:
                    print(f"Error retrieving binary data: {e}")
                    return arg_data['value']
            else:
                return arg_data['value']
        elif "__nerd_data_reference" in arg_data:
            # For references to cloud storage
            data_id = arg_data["__nerd_data_reference"]
            s3_uri = arg_data.get("__nerd_s3_uri", "")
            print(f"Deserializing data reference: {data_id}")

            if s3_uri.startswith("s3://"):
                try:
                    import boto3
                    import io

                    parts = s3_uri[5:].split("/", 1)
                    if len(parts) == 2:
                        bucket = parts[0]
                        key = parts[1]

                        # Download the data
                        s3 = boto3.client('s3')
                        buffer = io.BytesIO()
                        s3.download_fileobj(bucket, key, buffer)
                        buffer.seek(0)
                        raw_data = buffer.read()
                        print(f"Retrieved data: {len(raw_data) / (1024 * 1024):.2f} MB")

                        # Try to decompress and unpickle the data
                        try:
                            decompressed_data = zlib.decompress(raw_data)
                            # Use cloudpickle for consistent deserialization
                            unpickled_data = cloudpickle.loads(decompressed_data)
                            print(f"Unpickled data of type: {type(unpickled_data).__name__}")
                            return unpickled_data
                        except Exception as unpickle_err:
                            print(f"Could not unpickle data: {unpickle_err}")
                            return raw_data
                except Exception as e:
                    print(f"Error retrieving data: {e}")
        else:
            # Regular dictionary
            return arg_data
    else:
        # Non-dictionary values
        return arg_data

# Debug function to get environment variables
def debug_env():
    env_vars = {}
    for key in os.environ:
        env_vars[key] = os.environ.get(key, 'NOT_SET')
    return env_vars

def run_with_args(func_name, args_serialized, kwargs_serialized):
    print(f"Cloud environment: {json.dumps(debug_env())}")

    # Will be replaced with actual function source
    # FUNCTION_SOURCE_PLACEHOLDER

    # Unpack all the arguments
    args = []
    for arg_data in args_serialized:
        args.append(deserialize_arg(arg_data))

    # Unpack all the keyword arguments
    kwargs = {}
    for key, arg_data in kwargs_serialized.items():
        kwargs[key] = deserialize_arg(arg_data)

    try:
        print(f"Starting cloud execution of {func_name}...")
        result = auto_reference_wrapper(eval(func_name), args, kwargs)
        print(f"Function execution completed successfully")

        try:
            print("Packaging results to send back...")
            # 1. Pickle the result
            result_pickled = pickle.dumps(result)
            # 2. Compress the pickled data
            result_compressed = zlib.compress(result_pickled)
            # 3. Base64 encode the compressed data
            result_encoded = base64.b64encode(result_compressed).decode('utf-8')
            print(f"Results packaged (size: {len(result_encoded)} characters)")

            result_json = f'{{"result_size": {len(result_encoded)}, "result": "{result_encoded}"}}'

            print("RESULT_MARKER_BEGIN")
            print(result_json)
            print("RESULT_MARKER_END")

            # Save to multiple paths for redundancy
            with open('/tmp/result.json', 'w') as f:
                f.write(result_json)
            print("Saved result to /tmp/result.json")

            try:
                alternative_paths = ['/mnt/data/result.json', './result.json']
                for alt_path in alternative_paths:
                    try:
                        with open(alt_path, 'w') as f:
                            f.write(result_json)
                        print(f"Also saved result to {alt_path}")
                    except:
                        pass
            except Exception as e:
                print(f"Error saving to alternative paths: {e}")

            sys.stdout.flush()
            time.sleep(5)
        except Exception as e:
            print(f"Error packaging results: {e}")
            print(traceback.format_exc())
            raise
    except Exception as e:
        print(f"EXECUTION ERROR: {e}")
        print(traceback.format_exc())
        raise