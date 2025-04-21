import pickle
import base64
import zlib
import json
import time
import os
import traceback
import sys

# This function unpacks the data we sent
def deserialize_arg(arg_data):
    if arg_data['type'] == 'data':
        try:
            # 1. Decode from base64
            binary_data = base64.b64decode(arg_data['value'])
            # 2. Decompress the data
            decompressed = zlib.decompress(binary_data)
            # 3. Unpickle to get original object
            return pickle.loads(decompressed)
        except Exception as e:
            print(f"Error deserializing: {e}")
            return arg_data['value']
    else:
        return arg_data['value']

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