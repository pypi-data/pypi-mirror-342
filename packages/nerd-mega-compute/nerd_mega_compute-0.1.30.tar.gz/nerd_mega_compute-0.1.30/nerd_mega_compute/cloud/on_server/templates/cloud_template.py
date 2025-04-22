import pickle
import base64
import zlib
import json
import time
import os
import traceback
import sys

# Debug utility function for diagnostics
def debug_arg_with_diagnostics(arg):
    """Print detailed diagnostic information about an argument to help troubleshoot serialization issues"""
    import sys
    import os
    
    # Create logs directory if it doesn't exist
    log_dir = '/tmp/nerd_debug'
    os.makedirs(log_dir, exist_ok=True)
    
    # Debug log file to persist data for troubleshooting
    log_file = f"{log_dir}/args_debug.log"
    
    # Save basic info about the argument
    arg_type = type(arg).__name__
    arg_str = str(arg)[:1000] if len(str(arg)) > 1000 else str(arg)
    
    # Log message to both stdout and file
    debug_msg = f"\n=========== ARGUMENT DIAGNOSTICS ===========\n"
    debug_msg += f"Type: {arg_type}\n"
    
    # Add type-specific diagnostics
    if isinstance(arg, dict):
        debug_msg += f"Dict keys: {list(arg.keys())}\n"
        
        # Special handling for specific astronomy data types
        if 'sources' in arg and 'positions' in arg and 'fluxes' in arg:
            debug_msg += f"ASTRONOMY DATA: Sparse catalog detected\n"
            debug_msg += f"- sources type: {type(arg['sources']).__name__}, length: {len(arg['sources'])}\n"
            debug_msg += f"- positions type: {type(arg['positions']).__name__}, shape: {getattr(arg['positions'], 'shape', 'unknown')}\n"
            debug_msg += f"- fluxes type: {type(arg['fluxes']).__name__}, length: {len(arg['fluxes'])}\n"
        
        elif 'model' in arg:
            debug_msg += f"ASTRONOMY DATA: ML model detected\n"
            debug_msg += f"- model type: {type(arg['model']).__name__}\n"
            if hasattr(arg['model'], 'predict'):
                debug_msg += f"- model has predict method\n"
            else:
                debug_msg += f"- model MISSING predict method\n"
                
        elif 'pixels' in arg:
            debug_msg += f"ASTRONOMY DATA: HEALPix map detected\n"
            debug_msg += f"- pixels type: {type(arg['pixels']).__name__}\n"
            if 'pixel_values' in arg:
                debug_msg += f"- pixel_values type: {type(arg['pixel_values']).__name__}\n"
            else:
                debug_msg += f"- pixel_values key MISSING\n"
    
    debug_msg += f"\nFirst 1000 chars of string representation:\n{arg_str}\n"
    debug_msg += f"===========================================\n"
    
    # Print to stdout
    print(debug_msg)
    
    # Also write to file
    with open(log_file, 'a') as f:
        f.write(debug_msg)
    
    return arg  # Return the arg unchanged for pass-through

# This function unpacks the data we sent
def deserialize_arg(arg_data):
    if isinstance(arg_data, dict) and 'type' in arg_data:
        if arg_data['type'] == 'data' or arg_data['type'] == 'cloudpickle':
            try:
                # 1. Decode from base64
                binary_data = base64.b64decode(arg_data['value'])
                # 2. Decompress the data if needed
                if arg_data['type'] == 'data':
                    decompressed = zlib.decompress(binary_data)
                else:
                    decompressed = binary_data
                # 3. Unpickle to get original object
                obj = pickle.loads(decompressed)
                
                # Process astronomy data types
                if isinstance(obj, dict):
                    # Handle sparse catalog - return the dictionary as is
                    # Don't try to convert to DataFrame here - just ensure the structure is correct
                    if 'sources' in obj and 'positions' in obj and 'fluxes' in obj:
                        print("Detected sparse catalog structure")
                        print(f"sources type: {type(obj['sources'])}, positions type: {type(obj['positions'])}, fluxes type: {type(obj['fluxes'])}")
                        print(f"sources length: {len(obj['sources'])}, positions shape: {getattr(obj['positions'], 'shape', 'unknown')}, fluxes length: {len(obj['fluxes'])}")
                        # Let the function handle DataFrame creation
                    
                    # Handle ML model
                    elif 'model' in obj and isinstance(obj['model'], bytes):
                        print("Unpickling model from bytes")
                        try:
                            obj['model'] = pickle.loads(obj['model'])
                            print(f"Unpickled model type: {type(obj['model'])}")
                        except Exception as e:
                            print(f"Error unpickling model: {e}")
                            traceback.print_exc()
                    
                    # Handle HEALPix map
                    elif 'pixels' in obj and 'pixel_values' not in obj:
                        print("Adding pixel_values to HEALPix map")
                        obj['pixel_values'] = obj['pixels']
                
                return obj
            except Exception as e:
                print(f"Error deserializing: {e}")
                traceback.print_exc()
                return arg_data['value']
        elif arg_data['type'] == 'bytes_reference':
            # ...existing code...
        else:
            return arg_data['value']
    elif isinstance(arg_data, dict) and "__nerd_data_reference" in arg_data:
        # ...existing code...
    else:
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