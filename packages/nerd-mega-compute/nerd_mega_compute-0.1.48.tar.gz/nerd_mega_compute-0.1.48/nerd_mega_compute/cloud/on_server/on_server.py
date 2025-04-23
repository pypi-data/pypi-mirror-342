import pickle
import base64
import zlib
import os
import pathlib

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

# Deserializer function
def deserialize_arg(arg_data):
    """
    Deserializes arguments passed to the cloud function

    Args:
        arg_data: The serialized argument data

    Returns:
        The deserialized Python object
    """
    if isinstance(arg_data, dict):
        if arg_data.get('type') == 'data':
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
        elif arg_data.get('type') == 'bytes_reference':
            # This is handled by the auto_reference_wrapper function
            # We return the reference as-is and let auto_reference_wrapper resolve it
            return arg_data
        else:
            return arg_data.get('value')
    return arg_data

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
def generate_cloud_code(source, func_name, serialized_args, serialized_kwargs, import_block):
    """
    Generates the complete cloud code to execute the function

    Args:
        source: Source code of the function to execute
        func_name: Name of the function
        serialized_args: Serialized positional arguments
        serialized_kwargs: Serialized keyword arguments
        import_block: Import statements block

    Returns:
        A string containing the complete cloud execution code
    """
    # Get template content from files
    cloud_template = get_cloud_template()
    universal_imports = get_universal_imports()
    auto_reference_code = get_auto_reference_code()
    execution_template = get_execution_template()

    # Extract the header part (everything before run_with_args function)
    header_end = cloud_template.find("def run_with_args")
    if header_end == -1:
        raise ValueError("Could not find 'def run_with_args' in cloud_template.py")

    header = cloud_template[:header_end].strip()

    # Replace placeholders in execution template
    execution_code = execution_template
    execution_code = execution_code.replace("ARG_PLACEHOLDER", repr(serialized_args))
    execution_code = execution_code.replace("KWARGS_PLACEHOLDER", repr(serialized_kwargs))
    execution_code = execution_code.replace("FUNC_NAME_PLACEHOLDER", func_name)

    # Building the final code structure
    final_code = [
        header,
        f'print(f"Cloud environment: {{json.dumps(debug_env())}}")',
        "# Auto-imported modules extracted from function code",
        universal_imports,
        import_block,
        "# Your original function is copied below (without the decorator)",
        source,
        "# Auto-reference handler",
        auto_reference_code,
        execution_code
    ]

    # Join all parts to create the final code
    return "\n\n".join(final_code)