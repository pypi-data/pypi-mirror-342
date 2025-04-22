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
def generate_cloud_code(function_code, function_name, serialized_args, serialized_kwargs, import_block):
    """
    Generates executable code for the cloud server.

    Args:
        function_code (str): The function code to execute
        function_name (str): The name of the function
        serialized_args (list): Serialized positional arguments
        serialized_kwargs (dict): Serialized keyword arguments
        import_block (str): Block of import statements needed by the function

    Returns:
        str: The complete code to execute on the cloud server
    """
    # Create the shell code that will be executed on the server
    cloud_template = f"""
{import_block}
import pickle
import base64
import zlib
import json
import io
import sys
import os
import traceback
import cloudpickle

def _deserialize_arg(arg_spec):
    \"\"\"Deserialize an argument from its serialized form\"\"\"
    if isinstance(arg_spec, dict) and 'type' in arg_spec and 'value' in arg_spec:
        arg_type = arg_spec['type']
        arg_value = arg_spec['value']

        if arg_type == 'cloudpickle':
            # Deserialize using our simplified cloudpickle approach
            try:
                # 1. Decode the base64 string
                binary_data = base64.b64decode(arg_value)
                # 2. Unpickle the binary data
                return cloudpickle.loads(binary_data)
            except Exception as e:
                print(f"Error deserializing cloudpickle: {{e}}")
                return arg_value

        elif arg_type == 'bytes_reference':
            # Handle reference to data in cloud storage
            try:
                import requests
                from time import sleep

                # Function to fetch data from cloud storage
                def fetch_from_storage(data_id):
                    api_key = os.environ.get('NERD_COMPUTE_API_KEY')
                    if not api_key:
                        print("ERROR: NERD_COMPUTE_API_KEY environment variable not set")
                        return None

                    url = "https://api.nerdcompute.com/data/large"
                    headers = {{'Content-Type': 'application/json', 'x-api-key': api_key}}
                    params = {{'dataId': data_id}}

                    # Try multiple times in case of network issues
                    for attempt in range(3):
                        try:
                            # Get presigned URL
                            response = requests.get(url, headers=headers, params=params)
                            if response.status_code != 200:
                                print(f"Error getting presigned URL, status: {{response.status_code}}")
                                sleep(1)
                                continue

                            result = response.json()
                            presigned_url = result.get('presignedUrl')
                            if not presigned_url:
                                print("No presigned URL in response")
                                return None

                            # Download file using presigned URL
                            download_response = requests.get(presigned_url)
                            if download_response.status_code != 200:
                                print(f"Error downloading file, status: {{download_response.status_code}}")
                                sleep(1)
                                continue

                            # Return raw binary data
                            return download_response.content
                        except Exception as e:
                            print(f"Error fetching data: {{e}}")
                            sleep(1)

                    return None

                # Get the data ID from the reference
                data_ref = arg_value.get('data_reference')
                if not data_ref:
                    return None

                # Fetch the data
                raw_data = fetch_from_storage(data_ref)
                if raw_data:
                    # Try to deserialize the data using cloudpickle
                    try:
                        return cloudpickle.loads(raw_data)
                    except Exception as e:
                        print(f"Error deserializing fetched data: {{e}}")
                        return raw_data
                return None
            except Exception as e:
                print(f"Error processing data reference: {{e}}")
                return None

        elif arg_type == 'string':
            return arg_value

        else:
            print(f"Unknown argument type: {{arg_type}}")
            return arg_value

    elif isinstance(arg_spec, dict) and '__nerd_data_reference' in arg_spec:
        # Handle reference objects for backward compatibility
        try:
            import requests
            from time import sleep

            data_id = arg_spec['__nerd_data_reference']

            # Function to fetch data from cloud storage (same as above)
            def fetch_from_storage(data_id):
                api_key = os.environ.get('NERD_COMPUTE_API_KEY')
                if not api_key:
                    print("ERROR: NERD_COMPUTE_API_KEY environment variable not set")
                    return None

                url = "https://api.nerdcompute.com/data/large"
                headers = {{'Content-Type': 'application/json', 'x-api-key': api_key}}
                params = {{'dataId': data_id}}

                for attempt in range(3):
                    try:
                        response = requests.get(url, headers=headers, params=params)
                        if response.status_code != 200:
                            print(f"Error getting presigned URL, status: {{response.status_code}}")
                            sleep(1)
                            continue

                        result = response.json()
                        presigned_url = result.get('presignedUrl')
                        if not presigned_url:
                            print("No presigned URL in response")
                            return None

                        download_response = requests.get(presigned_url)
                        if download_response.status_code != 200:
                            print(f"Error downloading file, status: {{download_response.status_code}}")
                            sleep(1)
                            continue

                        return download_response.content
                    except Exception as e:
                        print(f"Error fetching data: {{e}}")
                        sleep(1)

                return None

            # Fetch the data
            raw_data = fetch_from_storage(data_id)
            if raw_data:
                # Try to deserialize the data
                try:
                    return cloudpickle.loads(raw_data)
                except Exception as e:
                    print(f"Error deserializing fetched data: {{e}}")
                    return raw_data
            return None
        except Exception as e:
            print(f"Error processing data reference: {{e}}")
            return None

    return arg_spec

def _serialize_result(result):
    \"\"\"Serialize the result for transport back to the client\"\"\"
    try:
        # Using standard pickle/zlib/base64 for the result as that's expected on client side
        serialized = base64.b64encode(zlib.compress(pickle.dumps(result))).decode('utf-8')
        result_size = len(serialized)
        return {{'result': serialized, 'result_size': result_size}}
    except Exception as e:
        print(f"Error serializing result: {{e}}")
        traceback_str = traceback.format_exc()
        return {{'error': str(e), 'traceback': traceback_str}}

# Define the function we're executing
{function_code}

# Deserialize arguments
args = []
for arg_spec in {serialized_args}:
    args.append(_deserialize_arg(arg_spec))

kwargs = {{}}
for key, arg_spec in {serialized_kwargs}.items():
    kwargs[key] = _deserialize_arg(arg_spec)

# Execute the function with the deserialized arguments
try:
    result = {function_name}(*args, **kwargs)

    # Serialize and output the result
    result_json = _serialize_result(result)
    print("RESULT_MARKER_BEGIN", flush=True)
    print(json.dumps(result_json), flush=True)
    print("RESULT_MARKER_END", flush=True)
except Exception as e:
    error_json = {{
        'error': str(e),
        'traceback': traceback.format_exc()
    }}
    print("RESULT_MARKER_BEGIN", flush=True)
    print(json.dumps(error_json), flush=True)
    print("RESULT_MARKER_END", flush=True)
"""
    return cloud_template