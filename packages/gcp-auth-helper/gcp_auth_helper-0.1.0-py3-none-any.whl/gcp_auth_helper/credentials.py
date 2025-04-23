import logging
from google.auth import default as google_auth_default
from google.auth.transport.requests import Request
from google.auth.credentials import Credentials
from google.auth import compute_engine
from .constants import ENVIRONMENT

_cached_credentials: Credentials | None = None

def get_gcp_credentials() -> Credentials:
    """
    Returns a cached Google Cloud credential object.

    In 'prod' or 'staging', it uses Compute Engine credentials.
    Otherwise, it uses local credentials from gcloud SDK.
    """
    global _cached_credentials

    if _cached_credentials is not None:
        return _cached_credentials

    if ENVIRONMENT in ["prod", "production", "staging"]:
        logging.info("✅ Executing in production environment (using Compute Engine Credentials)")
        _cached_credentials = compute_engine.Credentials()
    else:
        logging.info("⚙️ Using local environment...")
        _cached_credentials, _ = google_auth_default()
        if not _cached_credentials.valid or _cached_credentials.expired:
            _cached_credentials.refresh(Request())

    return _cached_credentials
