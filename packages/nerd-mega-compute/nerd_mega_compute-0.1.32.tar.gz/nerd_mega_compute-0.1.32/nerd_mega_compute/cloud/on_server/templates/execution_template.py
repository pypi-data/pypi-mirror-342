# This template handles the execution of user functions on the cloud server

def run_with_args():
    """Main function to execute the user's code with the provided arguments"""
    print("Starting cloud execution...")
    
    try:
        # Deserialize the arguments
        serialized_args = ARG_PLACEHOLDER
        serialized_kwargs = KWARGS_PLACEHOLDER
        func_name = FUNC_NAME_PLACEHOLDER
        
        print(f"Deserializing {len(serialized_args)} args and {len(serialized_kwargs)} kwargs...")
        
        # Deserialize each argument
        args = []
        for i, arg_data in enumerate(serialized_args):
            print(f"Deserializing arg {i}...")
            deserialized_arg = deserialize_arg(arg_data)
            args.append(deserialized_arg)
        
        # Deserialize each keyword argument
        kwargs = {}
        for key, arg_data in serialized_kwargs.items():
            print(f"Deserializing kwarg {key}...")
            deserialized_arg = deserialize_arg(arg_data)
            kwargs[key] = deserialized_arg
        
        # Get the function to execute
        func = globals().get(func_name)
        if not func:
            raise ValueError(f"Function {func_name} not found in global namespace")
        
        print(f"Executing {func_name} with {len(args)} args and {len(kwargs)} kwargs...")
        
        # Wrap the function to handle data references
        result = auto_reference_wrapper(func, args, kwargs)
        
        print(f"Function executed successfully, result type: {type(result).__name__}")
        
        # Serialize the result for returning to the client
        serialized_result = serialize_result(result)
        
        # Print result with markers for easier extraction
        print("RESULT_MARKER_BEGIN")
        print(json.dumps(serialized_result))
        print("RESULT_MARKER_END")
        
        # Also save the result to a file for alternative retrieval methods
        try:
            with open('/tmp/result.json', 'w') as f:
                f.write(json.dumps(serialized_result))
            print("Saved result to /tmp/result.json")
        except Exception as e:
            print(f"Warning: Could not save result to file: {e}")
        
        return result
        
    except Exception as e:
        error_message = str(e)
        error_traceback = traceback.format_exc()
        
        print(f"Error executing function: {error_message}")
        print(error_traceback)
        
        # Print error with markers for easier extraction
        print("RESULT_MARKER_BEGIN")
        print(json.dumps({
            "error": error_message,
            "details": error_traceback
        }))
        print("RESULT_MARKER_END")
        
        # Also save the error to a file for alternative retrieval methods
        try:
            with open('/tmp/result.json', 'w') as f:
                f.write(json.dumps({
                    "error": error_message,
                    "details": error_traceback
                }))
            print("Saved error to /tmp/result.json")
        except Exception as e:
            print(f"Warning: Could not save error to file: {e}")
        
        return None

# Execute the function when this script is run
if __name__ == "__main__":
    run_with_args()