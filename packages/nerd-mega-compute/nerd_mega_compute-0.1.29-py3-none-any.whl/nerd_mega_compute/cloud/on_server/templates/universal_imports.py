# Fallback imports for common libraries
try:
    import numpy as np
except ImportError:
    pass
try:
    import pandas as pd
except ImportError:
    pass
try:
    import matplotlib.pyplot as plt
except ImportError:
    pass
try:
    # Import pickle (always needed for serialization/deserialization)
    import pickle
except ImportError:
    pass
try:
    # Import cloudpickle as an optional import (used in some environments)
    import cloudpickle
except ImportError:
    pass

# Astronomy-specific imports for the test cases
try:
    from astropy.io import fits
except ImportError:
    pass
try:
    from astropy.table import Table
except ImportError:
    pass
try:
    import healpy as hp
except ImportError:
    pass