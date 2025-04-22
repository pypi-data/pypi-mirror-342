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