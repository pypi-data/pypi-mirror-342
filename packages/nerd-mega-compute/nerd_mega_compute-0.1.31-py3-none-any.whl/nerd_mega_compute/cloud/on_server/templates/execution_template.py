# This template handles the argument unpacking and execution of the function
# For astronomy functions, use patched versions
try:
    # Add directory to path to ensure patch can be imported
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    from catalog_patch import process_sparse_catalog as patched_sparse_catalog
    print("Successfully imported patched sparse catalog function")
except ImportError as e:
    print(f"Patched sparse catalog function not available: {e}")
    patched_sparse_catalog = None

# Unpack all the arguments
args = []
for arg_data in ARG_PLACEHOLDER:
    deserialized_arg = deserialize_arg(arg_data)
    
    # Apply diagnostics to log the argument details
    deserialized_arg = debug_arg_with_diagnostics(deserialized_arg)
    
    # Handle special cases for astronomy data
    if isinstance(deserialized_arg, dict):
        # Handle special cases for astronomy data types
        if 'sources' in deserialized_arg and 'positions' in deserialized_arg and 'fluxes' in deserialized_arg:
            print("Processing sparse catalog before function call")
        elif 'model' in deserialized_arg and isinstance(deserialized_arg['model'], bytes):
            print("Unpickling model from bytes")
            try:
                deserialized_arg['model'] = pickle.loads(deserialized_arg['model'])
                print(f"Successfully unpickled model of type: {type(deserialized_arg['model'])}")
            except Exception as e:
                print(f"Error unpickling model: {e}")
        elif 'pixels' in deserialized_arg:
            print("Processing HEALPix map before function call")
            if 'pixel_values' not in deserialized_arg:
                print("Adding pixel_values key with pixels data")
                deserialized_arg['pixel_values'] = deserialized_arg['pixels']
    
    args.append(deserialized_arg)

# Unpack all the keyword arguments
kwargs = {}
for key, arg_data in KWARGS_PLACEHOLDER.items():
    deserialized_arg = deserialize_arg(arg_data)
    deserialized_arg = debug_arg_with_diagnostics(deserialized_arg)
    kwargs[key] = deserialized_arg

try:
    print(f"Starting cloud execution of FUNC_NAME_PLACEHOLDER...")
    
    # Special handling for specific functions
    if "process_sparse_catalog" in FUNC_NAME_PLACEHOLDER and patched_sparse_catalog is not None:
        print("Using patched version of process_sparse_catalog")
        result = patched_sparse_catalog(*args, **kwargs)
    elif "evaluate_astronomy_model" in FUNC_NAME_PLACEHOLDER:
        print("Special handling for astronomy model evaluation")
        # Make sure the model is unpickled
        if len(args) > 0 and isinstance(args[0], dict) and 'model' in args[0]:
            if isinstance(args[0]['model'], bytes):
                import pickle
                print("Unpickling model from bytes")
                try:
                    args[0]['model'] = pickle.loads(args[0]['model'])
                    print(f"Successfully unpickled model: {type(args[0]['model'])}")
                except Exception as e:
                    print(f"Error unpickling model: {e}")
        result = auto_reference_wrapper(FUNC_NAME_PLACEHOLDER, args, kwargs)
    elif "process_healpix_map" in FUNC_NAME_PLACEHOLDER:
        print("Special handling for HEALPix map processing")
        # Make sure pixel_values is set
        if len(args) > 0 and isinstance(args[0], dict) and 'pixels' in args[0]:
            if 'pixel_values' not in args[0]:
                args[0]['pixel_values'] = args[0]['pixels']
                print("Added pixel_values from pixels")
        result = auto_reference_wrapper(FUNC_NAME_PLACEHOLDER, args, kwargs)
    else:
        # Use the standard function
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