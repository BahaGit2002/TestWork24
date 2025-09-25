from pymongo import MongoClient
from app.config import settings
import logging

logger = logging.getLogger(__name__)

try:
    client = MongoClient(settings.MONGODB_URL)
    db = client["quotes_db"]
    db.command("ping")
    logger.info("Connected to MongoDB successfully!")
except ConnectionError as e:
    logger.error(f"Failed to connect to MongoDB: {e}")
    raise

quotes_collection = db["quotes"]


def close_connection():
    client.close()
    logger.info("MongoDB connection closed.")
