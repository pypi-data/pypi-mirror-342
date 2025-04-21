import sys
import time
import requests
import traceback
import signal
import atexit

from ..config import NERD_COMPUTE_ENDPOINT, DEBUG_MODE
from .auth import get_api_key
from ..utils import debug_print

# Global dictionary to track active jobs for cancellation
_active_jobs = {}

def cancel_job(job_id, api_key=None):
    """
    Cancel a running cloud job by its ID.

    Args:
        job_id (str): The ID of the job to cancel
        api_key (str, optional): API key for authentication. If not provided, will try to get from config.

    Returns:
        bool: True if cancellation was successful, False otherwise
    """
    if not api_key:
        api_key = get_api_key()
        if not api_key:
            print("❌ No API key found. Job cancellation failed.")
            return False

    print(f"🛑 Cancelling job {job_id}...")

    try:
        headers = {
            "Content-Type": "application/json",
            "x-api-key": api_key
        }

        response = requests.delete(
            NERD_COMPUTE_ENDPOINT,
            headers=headers,
            params={"jobId": job_id},
            timeout=10
        )

        debug_print(f"DELETE response status: {response.status_code}")
        debug_print(f"DELETE response body: {response.text}")

        if response.status_code == 200:
            print("✅ Job cancelled successfully")
            return True
        elif response.status_code == 404:
            print("❌ Job not found or already completed")
            return False
        elif response.status_code == 409:
            print("⚠️ Job already completed or failed")
            return False
        else:
            print(f"❌ Job cancellation failed with status {response.status_code}")
            if DEBUG_MODE:
                try:
                    error_data = response.json()
                    print(f"Error details: {error_data.get('details', 'No details provided')}")
                except:
                    print(f"Response: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ Error during job cancellation: {e}")
        if DEBUG_MODE:
            traceback.print_exc()
        return False

def _sigint_handler(sig, frame):
    """Handle CTRL+C by cancelling active jobs."""
    print("\n⚠️ CTRL+C detected, cancelling active jobs...")

    if not _active_jobs:
        print("No active jobs to cancel.")
        sys.exit(1)

    api_key = get_api_key()
    for job_id in list(_active_jobs.keys()):
        cancel_job(job_id, api_key)

    print("Exiting...")
    sys.exit(1)

# Register the SIGINT handler
signal.signal(signal.SIGINT, _sigint_handler)

def _cleanup_active_jobs():
    """Clean up the active jobs dictionary on exit."""
    _active_jobs.clear()

atexit.register(_cleanup_active_jobs)

def list_active_jobs():
    """
    List all active jobs currently running.

    Returns:
        dict: Dictionary of active jobs with their details
    """
    if not _active_jobs:
        print("No active jobs running.")
        return {}

    print(f"Active jobs ({len(_active_jobs)}):")
    print("=" * 60)
    for job_id, job_info in _active_jobs.items():
        elapsed = int(time.time() - job_info["start_time"])
        print(f"Job ID: {job_id}")
        print(f"Function: {job_info['function_name']}")
        if job_info.get("batch_job_id"):
            print(f"Batch Job ID: {job_info['batch_job_id']}")
        print(f"Running for: {elapsed} seconds")
        print("-" * 60)

    return _active_jobs

def cancel_all_jobs():
    """
    Cancel all active jobs.

    Returns:
        int: Number of jobs successfully cancelled
    """
    if not _active_jobs:
        print("No active jobs to cancel.")
        return 0

    print(f"Cancelling {len(_active_jobs)} active jobs...")

    api_key = get_api_key()
    if not api_key:
        print("❌ No API key found. Job cancellation failed.")
        return 0

    cancelled_count = 0
    for job_id in list(_active_jobs.keys()):
        if cancel_job(job_id, api_key):
            cancelled_count += 1

    return cancelled_count
