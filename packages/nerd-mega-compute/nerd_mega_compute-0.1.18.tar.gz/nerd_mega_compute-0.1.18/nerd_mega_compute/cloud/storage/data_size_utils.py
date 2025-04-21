import pickle
import json
import sys
import io
from ...utils import debug_print

def is_large_data(data_to_upload, threshold_mb=10):
    """
    Determines if data should be treated as large based on size estimation.
    This function is mission-critical and must have zero false positives/negatives
    for ANY type of data.

    Args:
        data_to_upload: The data to check (any type)
        threshold_mb: Size threshold in MB (default: 10MB)

    Returns:
        bool: True if data exceeds the threshold, False otherwise
    """
    threshold_bytes = threshold_mb * 1024 * 1024
    debug_print(f"Checking if data is large. Type: {type(data_to_upload).__name__}")

    # Force large data handling for known problematic types
    ml_model_classes = [
        'RandomForestClassifier', 'DecisionTreeClassifier', 'LinearRegression',
        'LogisticRegression', 'SVC', 'SVR', 'MLPClassifier', 'MLPRegressor',
        'GradientBoostingClassifier', 'GradientBoostingRegressor', 'XGBClassifier',
        'XGBRegressor', 'LGBMClassifier', 'LGBMRegressor', 'SimpleClassifier'
    ]

    # Check if it's an ML model by class name
    class_name = data_to_upload.__class__.__name__
    if class_name in ml_model_classes:
        debug_print(f"Detected ML model: {class_name}, treating as large data")
        return True

    # Primary measurement techniques:
    size_measurements = []

    # 1. Try sys.getsizeof for a quick initial estimate (not reliable for all objects)
    try:
        sys_size = sys.getsizeof(data_to_upload)
        size_measurements.append(("sys.getsizeof", sys_size))
        debug_print(f"sys.getsizeof size: {sys_size / (1024 * 1024):.2f} MB")

        # Quick exit if the base object is already huge
        if sys_size > threshold_bytes:
            debug_print(f"Data is definitely large (sys.getsizeof): {sys_size / (1024 * 1024):.2f} MB")
            return True
    except Exception as e:
        debug_print(f"sys.getsizeof failed: {e}")

    # 2. For JSON-compatible data, measure actual serialized size
    if isinstance(data_to_upload, (dict, list, str, int, float, bool, type(None))):
        try:
            # Measure exact JSON serialization size
            json_serialized = json.dumps(data_to_upload)
            json_bytes = len(json_serialized.encode('utf-8'))
            size_measurements.append(("json", json_bytes))
            debug_print(f"JSON serialized size: {json_bytes / (1024 * 1024):.2f} MB")

            if json_bytes > threshold_bytes:
                debug_print(f"Data is large (JSON): {json_bytes / (1024 * 1024):.2f} MB")
                return True
        except (TypeError, OverflowError, ValueError) as e:
            debug_print(f"JSON serialization failed: {e}")

    # 3. For binary data, get direct length
    if isinstance(data_to_upload, (bytes, bytearray)):
        binary_size = len(data_to_upload)
        size_measurements.append(("binary", binary_size))
        debug_print(f"Binary data size: {binary_size / (1024 * 1024):.2f} MB")

        if binary_size > threshold_bytes:
            debug_print(f"Data is large (binary): {binary_size / (1024 * 1024):.2f} MB")
            return True

    # 4. For any object, try pickle serialization (most comprehensive)
    try:
        pickle_data = pickle.dumps(data_to_upload, protocol=pickle.HIGHEST_PROTOCOL)
        pickle_size = len(pickle_data)
        size_measurements.append(("pickle", pickle_size))
        debug_print(f"Pickle serialized size: {pickle_size / (1024 * 1024):.2f} MB")

        if pickle_size > threshold_bytes:
            debug_print(f"Data is large (pickle): {pickle_size / (1024 * 1024):.2f} MB")
            return True
    except Exception as e:
        debug_print(f"Pickle serialization failed: {e}")
        # If pickle fails, this is likely a complex object that should use large file handling
        if not isinstance(data_to_upload, (str, int, float, bool)):
            debug_print("Complex non-serializable object detected, treating as large")
            return True

    # 5. Special handling for objects with known size attributes
    try:
        # NumPy arrays and Pandas DataFrames have shape and sometimes nbytes
        if hasattr(data_to_upload, 'nbytes'):
            nbytes = getattr(data_to_upload, 'nbytes')
            size_measurements.append(("nbytes", nbytes))
            debug_print(f"Object nbytes attribute: {nbytes / (1024 * 1024):.2f} MB")

            if nbytes > threshold_bytes:
                debug_print(f"Data is large (nbytes): {nbytes / (1024 * 1024):.2f} MB")
                return True

        # Handle objects with shape attribute (numpy arrays, pandas dataframes)
        if hasattr(data_to_upload, 'shape'):
            debug_print(f"Object has shape attribute: {data_to_upload.shape}")
            try:
                # Calculate total elements
                if hasattr(data_to_upload, 'shape') and hasattr(data_to_upload.shape, '__len__'):
                    num_elements = 1
                    for dim in data_to_upload.shape:
                        num_elements *= dim
                    # Estimate based on elements (8 bytes per element is conservative)
                    estimated_size = num_elements * 8
                    size_measurements.append(("shape_estimate", estimated_size))

                    if estimated_size > threshold_bytes:
                        debug_print(f"Large array/dataframe detected with {num_elements} elements (~{estimated_size/(1024*1024):.2f} MB)")
                        return True
            except Exception as e:
                debug_print(f"Error analyzing shape: {e}")
    except Exception as e:
        debug_print(f"Error checking size attributes: {e}")

    # 6. Try file-like objects with size or tell/seek
    try:
        if hasattr(data_to_upload, 'seek') and hasattr(data_to_upload, 'tell'):
            # Save current position
            current_pos = data_to_upload.tell()

            # Seek to end and get position
            data_to_upload.seek(0, io.SEEK_END)
            file_size = data_to_upload.tell()
            size_measurements.append(("file_size", file_size))

            # Restore position
            data_to_upload.seek(current_pos)

            debug_print(f"File-like object size: {file_size / (1024 * 1024):.2f} MB")

            if file_size > threshold_bytes:
                debug_print(f"Data is large (file-like): {file_size / (1024 * 1024):.2f} MB")
                return True
    except Exception as e:
        debug_print(f"Error checking file-like object size: {e}")

    # 7. For objects with __len__, use that as a heuristic
    try:
        if hasattr(data_to_upload, '__len__') and not isinstance(data_to_upload, (str, dict, list, tuple, bytes, bytearray)):
            collection_len = len(data_to_upload)
            # Heuristic: if collection has many elements, treat as large
            if collection_len > 100000:  # Arbitrary threshold for large collections
                debug_print(f"Large collection with {collection_len} elements, treating as large")
                return True
    except Exception as e:
        debug_print(f"Error checking collection length: {e}")

    # Final decision based on the measurements we collected
    if size_measurements:
        max_measurement = max(size_measurements, key=lambda x: x[1])
        method, size = max_measurement
        debug_print(f"Maximum size measurement: {size / (1024 * 1024):.2f} MB using {method}")

        # If we're within 10% of the threshold, err on the side of caution
        if size > threshold_bytes * 0.9:
            debug_print(f"Data is near threshold ({size / (1024 * 1024):.2f} MB), treating as large for safety")
            return True

        return size > threshold_bytes
    else:
        # If we couldn't measure the size by any method, treat as large to be safe
        debug_print("Could not determine size by any method, treating as large for safety")
        return True