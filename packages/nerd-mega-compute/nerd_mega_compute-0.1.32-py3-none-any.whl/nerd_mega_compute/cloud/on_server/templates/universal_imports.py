# Common imports for scientific computing and data analysis
import os
import sys
import json
import time
import pickle
import base64
import zlib
import traceback
from io import BytesIO

# Standard scientific stack
try:
    import numpy as np
except ImportError:
    print("Warning: numpy not available")

try:
    import pandas as pd
except ImportError:
    print("Warning: pandas not available")

try:
    from scipy import signal
except ImportError:
    print("Warning: scipy.signal not available")

try:
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    import matplotlib.pyplot as plt
except ImportError:
    print("Warning: matplotlib not available")

# Astronomy libraries if needed
try:
    from astropy.io import fits
    from astropy.table import Table
    from astropy.wcs import WCS
    from astropy.coordinates import SkyCoord
    from astropy import units as u
except ImportError:
    print("Warning: astropy not available")

# Add AWS libraries for S3 access
try:
    import boto3
except ImportError:
    print("Warning: boto3 not available, S3 access will not work")