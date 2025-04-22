import os
from dotenv import load_dotenv, find_dotenv
from ..config import API_KEY, set_nerd_compute_api_key as config_set_key

def set_nerd_compute_api_key(api_key):
    """Set the API key for nerd-mega-compute."""
    config_set_key(api_key)

def get_api_key():
    """Get the API key from environment or global variable."""
    # First check if it's already set in the config
    if API_KEY:
        return API_KEY

    # Then try to load from .env file
    load_dotenv(find_dotenv(usecwd=True))
    env_api_key = os.getenv("NERD_COMPUTE_API_KEY") or os.getenv("API_KEY")
    if env_api_key:
        set_nerd_compute_api_key(env_api_key)
        return env_api_key

    return None
