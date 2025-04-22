# Special patched version of process_sparse_catalog
def process_sparse_catalog(catalog_data):
    """
    Process a large sparse astronomical catalog with proper DataFrame handling.
    
    Args:
        catalog_data: A dictionary containing sparse catalog data
        
    Returns:
        Dictionary with processing results
    """
    print("Running patched process_sparse_catalog function")
    import numpy as np
    from astropy.table import Table
    
    # Check if we got a dictionary with the expected structure
    if isinstance(catalog_data, dict) and 'sources' in catalog_data and 'positions' in catalog_data and 'fluxes' in catalog_data:
        try:
            print(f"Catalog has {len(catalog_data['sources'])} sources")
            print(f"Positions type: {type(catalog_data['positions'])}, shape: {getattr(catalog_data['positions'], 'shape', 'unknown')}")
            
            # Create the catalog using Table instead of DataFrame
            catalog = Table()
            catalog['source_id'] = catalog_data['sources']
            
            # Handle positions - ensure they're in the right format
            positions = catalog_data['positions']
            if isinstance(positions, np.ndarray) and len(positions.shape) == 2:
                catalog['ra'] = positions[:, 0]
                catalog['dec'] = positions[:, 1]
            else:
                # Convert list of lists/tuples to separate columns
                print("Converting positions to array columns")
                catalog['ra'] = [p[0] for p in positions]
                catalog['dec'] = [p[1] for p in positions]
            
            catalog['flux'] = catalog_data['fluxes']
            
            # The rest of the processing logic
            bright_condition = catalog['flux'] > 10
            high_z_condition = catalog['ra'] > 5.0  # Using RA > 5 as a proxy for high redshift
            
            bright_sources = catalog[bright_condition]
            high_z_sources = catalog[high_z_condition]
            
            result = {
                'total_objects': len(catalog),
                'bright_objects': len(bright_sources),
                'high_redshift_objects': len(high_z_sources),
                'bright_stats': {
                    'mean_magnitude': float(np.mean(bright_sources['flux'])),
                    'mean_redshift': float(np.mean(bright_sources['ra']) / 10)  # Simulated redshift
                },
                'high_z_stats': {
                    'mean_magnitude': float(np.mean(high_z_sources['flux'])),
                    'max_redshift': float(np.max(high_z_sources['ra']) / 1.0)  # Simulated redshift
                }
            }
            
            print("Successfully processed sparse catalog")
            return result
            
        except Exception as e:
            print(f"Error in patched process_sparse_catalog: {e}")
            import traceback
            traceback.print_exc()
            raise
    else:
        print(f"Invalid catalog data type: {type(catalog_data)}")
        if isinstance(catalog_data, dict):
            print(f"Keys: {list(catalog_data.keys())}")
        raise ValueError("Expected dictionary with sources, positions, and fluxes keys")