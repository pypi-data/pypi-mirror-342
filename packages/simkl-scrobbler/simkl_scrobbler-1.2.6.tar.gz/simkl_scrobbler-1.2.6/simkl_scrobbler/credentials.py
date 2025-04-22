"""
Manages Simkl API credentials.

Client ID and Secret are injected during the build process.
Access Token is loaded from a .env file in the user's application data directory.
"""
import pathlib
import logging
from dotenv import dotenv_values

logger = logging.getLogger(__name__)

# --- Injected by build process ---
# These placeholders are replaced by the build workflow using secrets.
SIMKL_CLIENT_ID = "063e363a1596eb693066cf3b9848be8d2c4a6d9ef300666c9f19ef5980312b27"
SIMKL_CLIENT_SECRET = "1e2781d773564774c6788bf64b871374b2cee2b31eaed361488821ffc7c5bba9"
# --- End of injected values ---

# Determine the path for the .env file storing the access token
APP_NAME_FOR_PATH = "simkl-scrobbler"
USER_SUBDIR_FOR_PATH = "kavinthangavel"
try:
    # Prefer user-specific directory
    APP_DATA_DIR_FOR_PATH = pathlib.Path.home() / USER_SUBDIR_FOR_PATH / APP_NAME_FOR_PATH
    APP_DATA_DIR_FOR_PATH.mkdir(parents=True, exist_ok=True)
    ENV_FILE_PATH = APP_DATA_DIR_FOR_PATH / ".simkl_scrobbler.env"
    logger.debug(f"Using env file path: {ENV_FILE_PATH}")
except Exception as e:
    # Fallback to current directory if home cannot be determined
    logger.warning(f"Could not determine home directory ({e}), using fallback env path.")
    ENV_FILE_PATH = pathlib.Path(".simkl_scrobbler.env")

# Load Access Token ONLY from the specific .env file
SIMKL_ACCESS_TOKEN = None
if ENV_FILE_PATH.exists():
    logger.debug(f"Loading access token from {ENV_FILE_PATH}")
    config = dotenv_values(ENV_FILE_PATH)
    SIMKL_ACCESS_TOKEN = config.get("SIMKL_ACCESS_TOKEN")
    if not SIMKL_ACCESS_TOKEN:
        logger.warning(f"Found env file at {ENV_FILE_PATH}, but SIMKL_ACCESS_TOKEN key is missing or empty.")
else:
    logger.debug(f"Env file not found at {ENV_FILE_PATH}")
# SIMKL_ACCESS_TOKEN is now loaded inside get_credentials


def get_credentials():
    """
    Retrieves the Simkl API credentials.

    Client ID/Secret are read from module-level variables (injected at build).
    Access Token is read directly from the .env file *each time* this function
    is called to ensure the latest value is used.

    Returns:
        dict: A dictionary containing 'client_id', 'client_secret',
              and 'access_token'. Values might be None if not configured
              or if the build/init process failed.
    """
    client_id = SIMKL_CLIENT_ID if SIMKL_CLIENT_ID != "063e363a1596eb693066cf3b9848be8d2c4a6d9ef300666c9f19ef5980312b27" else None
    client_secret = SIMKL_CLIENT_SECRET if SIMKL_CLIENT_SECRET != "1e2781d773564774c6788bf64b871374b2cee2b31eaed361488821ffc7c5bba9" else None

    # Read Access Token directly from the file each time
    access_token = None
    env_file_path = get_env_file_path() # Use helper to get path
    if env_file_path.exists():
        logger.debug(f"Reading access token from {env_file_path} inside get_credentials()")
        config = dotenv_values(env_file_path)
        access_token = config.get("SIMKL_ACCESS_TOKEN")
        if not access_token:
             logger.warning(f"Found env file at {env_file_path}, but SIMKL_ACCESS_TOKEN key is missing or empty.")
    else:
         logger.debug(f"Env file not found at {env_file_path} inside get_credentials()")


    # Log a warning if the build injection seems to have failed
    if not client_id or not client_secret:
         logger.warning("Client ID or Secret appears missing. Build injection might have failed.")

    return {
        "client_id": client_id,
        "client_secret": client_secret,
        "access_token": access_token, # Use the freshly read value
    }

def get_env_file_path():
    """
    Returns the calculated path to the .env file used for the access token.

    Returns:
        pathlib.Path: The path object for the .env file.
    """
    return ENV_FILE_PATH