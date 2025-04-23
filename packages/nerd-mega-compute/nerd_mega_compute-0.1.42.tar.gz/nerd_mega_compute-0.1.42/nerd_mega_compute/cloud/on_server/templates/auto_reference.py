# Automatically resolve references
def resolve_references(obj):
    print(f"[REFERENCE_DEBUG] resolve_references called with object type: {type(obj).__name__}")
    if isinstance(obj, dict):
        # Check for our reference format
        if "__nerd_data_reference" in obj:
            # Extract reference information
            data_id = obj["__nerd_data_reference"]
            s3_uri = obj.get("__nerd_s3_uri", "")
            size_mb = obj.get("__nerd_size_mb", "unknown")
            print(f"[REFERENCE_DEBUG] Auto-resolving data reference: {data_id}, S3 URI: {s3_uri}, Size: {size_mb}MB")

            # For S3 URIs, fetch directly from S3
            if s3_uri and s3_uri.startswith("s3://"):
                try:
                    from boto3 import client
                    import io
                    import pickle
                    import base64
                    import zlib
                    
                    # Parse bucket and key from S3 URI
                    parts = s3_uri[5:].split("/", 1)
                    if len(parts) == 2:
                        bucket = parts[0]
                        key = parts[1]
                        
                        print(f"[REFERENCE_DEBUG] Fetching from S3: bucket={bucket}, key={key}")
                        s3 = client('s3')
                        
                        # Download as stream to memory
                        buffer = io.BytesIO()
                        s3.download_fileobj(bucket, key, buffer)
                        buffer.seek(0)
                        data = buffer.read()
                        
                        data_size_mb = len(data) / (1024 * 1024)
                        print(f"[REFERENCE_DEBUG] Successfully downloaded {data_size_mb:.2f} MB from S3")
                        print(f"[REFERENCE_DEBUG] First 100 bytes: {data[:100]}")
                        
                        # Try multiple deserialization approaches
                        try:
                            # Approach 1: If this is zlib-compressed pickled data
                            try:
                                print("[REFERENCE_DEBUG] Trying zlib decompression + pickle approach")
                                decompressed = zlib.decompress(data)
                                print(f"[REFERENCE_DEBUG] Decompression successful, size: {len(decompressed) / (1024 * 1024):.2f} MB")
                                result = pickle.loads(decompressed)
                                print(f"[REFERENCE_DEBUG] Successfully unpickled data, result type: {type(result).__name__}")
                                
                                # Print detailed info about the result
                                if hasattr(result, '__dict__'):
                                    print(f"[REFERENCE_DEBUG] Result attributes: {dir(result)[:20]}")
                                elif isinstance(result, dict):
                                    print(f"[REFERENCE_DEBUG] Result keys: {list(result.keys())[:20]}")
                                elif hasattr(result, 'shape'):
                                    print(f"[REFERENCE_DEBUG] Result shape: {result.shape}")
                                
                                return result
                            except Exception as e:
                                print(f"[REFERENCE_DEBUG] zlib+pickle approach failed: {str(e)}")
                            
                            # Approach 2: Try direct pickle
                            try:
                                print("[REFERENCE_DEBUG] Trying direct pickle approach")
                                result = pickle.loads(data)
                                print(f"[REFERENCE_DEBUG] Successfully unpickled data directly, result type: {type(result).__name__}")
                                return result
                            except Exception as e:
                                print(f"[REFERENCE_DEBUG] Direct pickle approach failed: {str(e)}")
                            
                            # Approach 3: Try base64 + zlib + pickle
                            try:
                                print("[REFERENCE_DEBUG] Trying base64 + zlib + pickle approach")
                                decoded = base64.b64decode(data)
                                print(f"[REFERENCE_DEBUG] Base64 decoding successful, size: {len(decoded) / (1024 * 1024):.2f} MB")
                                decompressed = zlib.decompress(decoded)
                                print(f"[REFERENCE_DEBUG] Decompression successful, size: {len(decompressed) / (1024 * 1024):.2f} MB")
                                result = pickle.loads(decompressed)
                                print(f"[REFERENCE_DEBUG] Successfully unpickled data, result type: {type(result).__name__}")
                                return result
                            except Exception as e:
                                print(f"[REFERENCE_DEBUG] base64+zlib+pickle approach failed: {str(e)}")
                                
                            # Fallback: return raw bytes
                            print("[REFERENCE_DEBUG] All deserialization approaches failed, returning raw binary data")
                            return data
                        except Exception as e:
                            print(f"[REFERENCE_DEBUG] Error in deserializing data: {str(e)}")
                            return data
                except Exception as e:
                    print(f"[REFERENCE_DEBUG] Error accessing S3: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    # Continue to try other methods if S3 access fails
            
            # Try to fetch from API endpoint if available
            try:
                print("[REFERENCE_DEBUG] Attempting to fetch data through API")
                # Import helper function locally to avoid import cycles
                from nerd_mega_compute.cloud.helpers import fetch_nerd_data_reference
                result = fetch_nerd_data_reference(obj)
                print(f"[REFERENCE_DEBUG] API fetch successful, result type: {type(result).__name__}")
                return result
            except Exception as e:
                print(f"[REFERENCE_DEBUG] Error fetching data through API: {str(e)}")
                import traceback
                traceback.print_exc()
                # Return the reference object if all methods fail
                return obj
        elif "type" in obj and obj["type"] == "bytes_reference" and "value" in obj:
            # This is the format used in the serializer
            print("[REFERENCE_DEBUG] Found bytes_reference format")
            ref_data = obj["value"]
            if isinstance(ref_data, dict) and "data_reference" in ref_data:
                data_id = ref_data["data_reference"]
                s3_uri = ref_data.get("s3Uri", "")
                size_mb = ref_data.get("sizeMB", "unknown")
                print(f"[REFERENCE_DEBUG] Resolving bytes reference: {data_id}, S3 URI: {s3_uri}, Size: {size_mb}")
                
                # Try to fetch using helper
                try:
                    from nerd_mega_compute.cloud.helpers import fetch_nerd_data_reference
                    ref_obj = {
                        "__nerd_data_reference": data_id,
                        "__nerd_s3_uri": s3_uri,
                        "__nerd_size_mb": size_mb
                    }
                    result = fetch_nerd_data_reference(ref_obj)
                    print(f"[REFERENCE_DEBUG] Successfully fetched bytes_reference, result type: {type(result).__name__}")
                    return result
                except Exception as e:
                    print(f"[REFERENCE_DEBUG] Error fetching bytes reference: {str(e)}")
                    import traceback
                    traceback.print_exc()
            return obj
        else:
            # Regular dictionary, process each value recursively
            return {k: resolve_references(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        # Process each item in a list recursively
        return [resolve_references(item) for item in obj]
    
    # Return non-dict, non-list objects as is
    return obj

# Automatically resolve references before calling the function
def auto_reference_wrapper(func, args, kwargs):
    # Log function name and argument types for debugging
    print(f"[REFERENCE_DEBUG] auto_reference_wrapper called for function: {func.__name__}")
    print(f"[REFERENCE_DEBUG] Argument types: {[type(arg).__name__ for arg in args]}")
    print(f"[REFERENCE_DEBUG] Keyword arguments: {list(kwargs.keys())}")
    
    # Resolve references in arguments
    print("[REFERENCE_DEBUG] Resolving references in function arguments...")
    resolved_args = []
    for i, arg in enumerate(args):
        print(f"[REFERENCE_DEBUG] Processing arg[{i}], type: {type(arg).__name__}")
        resolved_arg = resolve_references(arg)
        print(f"[REFERENCE_DEBUG] Resolved arg[{i}], type: {type(resolved_arg).__name__}")
        resolved_args.append(resolved_arg)
    
    # Resolve references in keyword arguments
    resolved_kwargs = {}
    for k, v in kwargs.items():
        print(f"[REFERENCE_DEBUG] Processing kwarg[{k}], type: {type(v).__name__}")
        resolved_kwarg = resolve_references(v)
        print(f"[REFERENCE_DEBUG] Resolved kwarg[{k}], type: {type(resolved_kwarg).__name__}")
        resolved_kwargs[k] = resolved_kwarg
    
    # Log the final resolved argument types
    print(f"[REFERENCE_DEBUG] Final resolved argument types: {[type(arg).__name__ for arg in resolved_args]}")
    print(f"[REFERENCE_DEBUG] Final resolved keyword argument types: {[(k, type(v).__name__) for k, v in resolved_kwargs.items()]}")
    
    # Call the function with resolved arguments
    print(f"[REFERENCE_DEBUG] Calling function {func.__name__} with resolved arguments")
    try:
        result = func(*resolved_args, **resolved_kwargs)
        print(f"[REFERENCE_DEBUG] Function {func.__name__} executed successfully, result type: {type(result).__name__}")
        return result
    except Exception as e:
        print(f"[REFERENCE_DEBUG] Function {func.__name__} execution failed: {str(e)}")
        import traceback
        traceback.print_exc()
        raise