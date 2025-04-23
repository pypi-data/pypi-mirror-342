"""
NERD Mega Compute - Python Client

A client library for connecting to NERD Mega Compute's cloud compute infrastructure.
"""

from .config import set_debug_mode
from .cloud.auth import set_nerd_compute_api_key, get_api_key
from .cloud.compute import cloud_compute
from .cloud.storage.storage import upload_nerd_cloud_storage, fetch_nerd_cloud_storage
from .cloud.job import cancel_job, list_active_jobs, cancel_all_jobs
from .cloud.helpers import fetch_nerd_data_reference
from .utils import enable_debug_mode, check_job_manually

# Backward compatibility for API module users
get_nerd_compute_api_key = get_api_key

__all__ = [
    'set_nerd_compute_api_key',
    'get_nerd_compute_api_key',
    'cloud_compute',
    'upload_nerd_cloud_storage',
    'fetch_nerd_cloud_storage',
    'fetch_nerd_data_reference',
    'cancel_job',
    'list_active_jobs',
    'cancel_all_jobs',
    'enable_debug_mode',
    'set_debug_mode',
    'check_job_manually',
    'is_large_data',
]

# Package version
__version__ = '0.3.0'