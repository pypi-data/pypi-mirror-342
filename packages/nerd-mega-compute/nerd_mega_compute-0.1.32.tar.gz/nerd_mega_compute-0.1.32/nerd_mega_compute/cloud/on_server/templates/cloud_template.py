import pickle
import base64
import zlib
import json
import time
import os
import sys
import traceback

# Import S3 utilities for handling data references
try:
    import boto3
except ImportError:
    print("Warning: boto3 not available, S3 references will not work properly")

# For handling references
from io import BytesIO

# Setup environment variables for proper logging
os.environ['PYTHONUNBUFFERED'] = '1'

# Function to retrieve environment variables for debugging
def debug_env():
    """Returns a dictionary of environment variables"""
    env_vars = {}
    for key in os.environ:
        env_vars[key] = os.environ.get(key, 'NOT_SET')
    return env_vars

# Function to serialize results for returning to the client
def serialize_result(result):
    """
    Serialize a Python object for returning to the client
    
    Args:
        result: The Python object to serialize
        
    Returns:
        A JSON-serializable dictionary with the serialized result
    """
    try:
        # Step 1: Pickle the result (use protocol 4 for compatibility)
        pickled = pickle.dumps(result, protocol=4)
        
        # Step 2: Compress the pickled data
        compressed = zlib.compress(pickled)
        
        # Step 3: Base64 encode the compressed data
        encoded = base64.b64encode(compressed).decode('utf-8')
        
        # Calculate the size of the result
        result_size = len(pickled) / (1024 * 1024)
        
        return {
            "result": encoded,
            "result_size": result_size
        }
    except Exception as e:
        print(f"Error serializing result: {e}")
        traceback.print_exc()
        return {
            "error": str(e),
            "details": "Error occurred while serializing function result"
        }