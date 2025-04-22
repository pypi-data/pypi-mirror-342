import pickle
import base64
import zlib
import sys
import os
import json
import io
import cloudpickle
import pathlib
from ...utils import debug_print

# Get the path to the template files
TEMPLATE_DIR = pathlib.Path(__file__).parent / "templates"

def get_template_content(filename):
    """Reads a template file from the templates directory"""
    file_path = TEMPLATE_DIR / filename

    # Check if the file exists
    if not file_path.exists():
        raise FileNotFoundError(f"Template file {filename} not found at {file_path}")

    with open(file_path, 'r') as f:
        return f.read()

def get_universal_imports():
    """Returns the universal imports for common libraries"""
    return get_template_content("universal_imports.py")

def get_auto_reference_code():
    """Returns the code for auto-resolving references"""
    return get_template_content("auto_reference.py")

def get_execution_template():
    """Returns the execution template code"""
    return get_template_content("execution_template.py")

def get_cloud_template():
    """Returns the cloud template code"""
    return get_template_content("cloud_template.py")

# Debug utility
def debug_env():
    """Returns a dictionary of environment variables"""
    env_vars = {}
    for key in os.environ:
        env_vars[key] = os.environ.get(key, 'NOT_SET')
    return env_vars

# Save result to multiple paths for redundancy
def save_result_to_multiple_paths(result_json):
    """
    Saves results to multiple paths for redundancy

    Args:
        result_json: The JSON string to save
    """
    try:
        with open('/tmp/result.json', 'w') as f:
            f.write(result_json)
        print("Saved result to /tmp/result.json")

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

# Generate cloud code for function execution
def is_jsonable(x):
    """
    Checks if an object can be serialized to JSON.

    Args:
        x: Object to check

    Returns:
        bool: True if the object can be serialized, False otherwise
    """
    try:
        json.dumps(x)
        return True
    except (TypeError, OverflowError):
        return False

def generate_cloud_code(function_source, function_name, args, kwargs, import_block=None):
    """
    Generate code to be executed in the cloud environment.
    
    Args:
        function_source (str): Source code of the function to execute
        function_name (str): Name of the function
        args (list): Serialized positional arguments
        kwargs (dict): Serialized keyword arguments
        import_block (str, optional): Block of import statements

    Returns:
        str: Generated code ready for cloud execution
    """
    template = """
import os
import sys
import json
import base64
import pickle
import zlib
import traceback
import cloudpickle
from datetime import datetime, date
import numpy as np

# Additional imports for the function
{imports}

# Function definition
{function_source}

# Helper function to deserialize arguments
def deserialize_object(obj):
    if isinstance(obj, dict) and 'type' in obj:
        if obj['type'] == 'cloudpickle':
            # Cloudpickle serialized object
            try:
                pickled = base64.b64decode(obj['value'])
                return cloudpickle.loads(pickled)
            except Exception as e:
                print(f"Error deserializing cloudpickle object: {{e}}")
                return None
        elif obj['type'] == 'bytes_reference':
            # Reference to large binary data in S3
            try:
                import boto3
                s3_uri = obj['value'].get('s3Uri', '')
                if s3_uri.startswith('s3://'):
                    parts = s3_uri.replace('s3://', '').split('/', 1)
                    if len(parts) == 2:
                        bucket = parts[0]
                        key = parts[1]
                        s3 = boto3.client('s3')
                        response = s3.get_object(Bucket=bucket, Key=key)
                        return response['Body'].read()
                return f"Could not load S3 reference: {{s3_uri}}"
            except Exception as e:
                print(f"Error retrieving binary data from S3: {{e}}")
                return None
        elif obj['type'] == 'string':
            # Simple string value
            return obj['value']
        else:
            # Unknown type
            return obj['value']
    elif isinstance(obj, list):
        # Recursively deserialize lists
        return [deserialize_object(item) for item in obj]
    elif isinstance(obj, dict):
        # Recursively deserialize dictionaries
        return {{k: deserialize_object(v) for k, v in obj.items()}}
    return obj

# Test if an object can be JSON serialized
def is_jsonable(x):
    try:
        json.dumps(x)
        return True
    except (TypeError, OverflowError):
        return False

# Helper function to convert numpy arrays and other non-serializable objects to Python native types
def make_json_serializable(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, (np.bool_)):
        return bool(obj)
    elif isinstance(obj, (datetime, date)):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {{k: make_json_serializable(v) for k, v in obj.items()}}
    elif isinstance(obj, (list, tuple)):
        return [make_json_serializable(x) for x in obj]
    else:
        # For other types, try to see if it has a __dict__ or can be cast to str
        try:
            if hasattr(obj, '__dict__'):
                return {{'__custom_object__': True, 'class': obj.__class__.__name__, 'attributes': make_json_serializable(obj.__dict__)}}
            else:
                return str(obj)
        except:
            return str(obj)

# Deserialize arguments
args = {args}
kwargs = {kwargs}

deserialized_args = deserialize_object(args)
deserialized_kwargs = deserialize_object(kwargs)

# Set up result variable in global namespace
result = None

# Execute the function
try:
    print(f"Executing {function_name} with {{len(deserialized_args)}} args and {{len(deserialized_kwargs)}} kwargs")
    function_result = {function_name}(*deserialized_args, **deserialized_kwargs)
    
    # Save the result for the entrypoint script to find
    result = function_result
    
    # Also save to a file for the entrypoint script
    with open('/tmp/result.json', 'w') as f:
        try:
            # Try to serialize result directly
            if is_jsonable(function_result):
                json.dump(function_result, f)
                print("Result saved as direct JSON")
            else:
                # Convert non-serializable objects
                serializable_result = make_json_serializable(function_result)
                json.dump(serializable_result, f)
                print("Result saved as converted JSON")
        except Exception as json_err:
            # If JSON conversion fails, fallback to string representation
            print(f"JSON serialization failed: {{json_err}}")
            json.dump({{"string_result": str(function_result)}}, f)
            print("Result saved as string representation")
            
    print("✅ Function execution successful")
    
    # Add a marker for easier parsing
    result_marker = {{"status": "success", "message": "Function executed successfully"}}
    print(f"RESULT_MARKER_BEGIN\\n{{json.dumps(result_marker)}}\\nRESULT_MARKER_END")
    
except Exception as e:
    error_message = str(e)
    error_traceback = traceback.format_exc()
    print(f"❌ Error executing function: {{error_message}}")
    print(error_traceback)
    
    # Write error to result file
    with open('/tmp/result.json', 'w') as f:
        json.dump({{"error": error_message, "traceback": error_traceback}}, f)
    
    # Add a marker for easier parsing
    error_marker = {{"status": "error", "error": error_message}}
    print(f"RESULT_MARKER_BEGIN\\n{{json.dumps(error_marker)}}\\nRESULT_MARKER_END")
"""
    # Use provided import block or default to basic imports
    import_block = import_block or "import numpy as np\nimport pandas as pd"
    
    # Format the template with the function source and arguments
    formatted_code = template.format(
        imports=import_block,
        function_source=function_source,
        function_name=function_name,
        args=json.dumps(args),
        kwargs=json.dumps(kwargs)
    )
    
    return formatted_code