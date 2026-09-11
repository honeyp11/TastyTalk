import time
import logging

try:
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
except ImportError:
    MongoClient = None

from config.settings import resolve_mongo_uri, DB_NAME

logger = logging.getLogger(__name__)

_mongo_client = None
_last_attempt_time = 0.0
_connection_failed = False
_COOLDOWN_SECONDS = 90.0  # Cooldown between failed reconnect attempts to prevent UI stalls

def get_mongo_client(timeout_ms: int = 1200, force_retry: bool = False):
    """
    Returns a cached PyMongo client singleton with cooldown on failures to prevent UI freezing.
    """
    global _mongo_client, _last_attempt_time, _connection_failed

    if MongoClient is None:
        return None

    if _mongo_client is not None:
        return _mongo_client


    now = time.time()
    if not force_retry and _connection_failed and (now - _last_attempt_time < _COOLDOWN_SECONDS):
        # Database is offline; immediately return None without stalling Streamlit
        return None

    _last_attempt_time = now
    uri = resolve_mongo_uri()
    try:
        client = MongoClient(
            uri,
            serverSelectionTimeoutMS=timeout_ms,
            connectTimeoutMS=timeout_ms
        )
        # Fast ping test
        client.admin.command("ping")
        _mongo_client = client
        _connection_failed = False
        return _mongo_client
    except Exception as e:
        logger.warning(f"MongoDB connection failed (falling back to in-memory mode): {e}")
        _mongo_client = None
        _connection_failed = True
        return None

def get_db():
    """
    Returns the application database instance, or None if disconnected.
    """
    client = get_mongo_client()
    if client is not None:
        try:
            return client[DB_NAME]
        except Exception:
            return None
    return None

def is_db_connected() -> bool:
    """
    Quickly verifies if MongoDB is reachable without blocking UI.
    """
    client = get_mongo_client(timeout_ms=800)
    return client is not None

