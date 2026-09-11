import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from config.settings import resolve_mongo_uri, DB_NAME

logger = logging.getLogger(__name__)

_mongo_client = None

def get_mongo_client(timeout_ms: int = 2000):
    """
    Returns a cached PyMongo client singleton with short server selection timeout.
    """
    global _mongo_client
    if _mongo_client is None:
        uri = resolve_mongo_uri()
        try:
            _mongo_client = MongoClient(
                uri,
                serverSelectionTimeoutMS=timeout_ms,
                connectTimeoutMS=timeout_ms
            )
            # Fast ping test
            _mongo_client.admin.command("ping")
        except (ConnectionFailure, ServerSelectionTimeoutError, Exception) as e:
            logger.warning(f"MongoDB connection failed: {e}")
            _mongo_client = None
            return None
    return _mongo_client

def get_db():
    """
    Returns the application database instance, or None if disconnected.
    """
    client = get_mongo_client()
    if client is not None:
        return client[DB_NAME]
    return None

def is_db_connected() -> bool:
    """
    Quickly verifies if MongoDB is reachable.
    """
    try:
        client = get_mongo_client(timeout_ms=1000)
        if client is not None:
            client.admin.command("ping")
            return True
        return False
    except Exception:
        return False
