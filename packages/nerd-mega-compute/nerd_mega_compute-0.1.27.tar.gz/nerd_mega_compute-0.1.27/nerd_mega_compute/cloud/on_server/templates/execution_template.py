# This template handles the argument unpacking and execution of the function
# Import debug utilities
from debug_utils import debug_arg_with_diagnostics

# Unpack all the arguments
args = []
for arg_data in ARG_PLACEHOLDER:
    deserialized_arg = deserialize_arg(arg_data)
    
    # Apply diagnostics to log the argument details
    debug_arg_with_diagnostics(deserialized_arg)
    
    args.append(deserialized_arg)

# Unpack all the keyword arguments
kwargs = {}
for key, arg_data in KWARGS_PLACEHOLDER.items():
    deserialized_arg = deserialize_arg(arg_data)
    
    # Apply diagnostics to log the argument details
    debug_arg_with_diagnostics(deserialized_arg)
    
    kwargs[key] = deserialized_arg

try:
    print(f"Starting cloud execution of FUNC_NAME_PLACEHOLDER...")
    result = auto_reference_wrapper(FUNC_NAME_PLACEHOLDER, args, kwargs)
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