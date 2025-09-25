import logging
from datetime import datetime

from celery import Celery
from pymongo import MongoClient

from app.config import settings
from app.database import quotes_collection, close_connection
from app.scraper import scrape_quotes_from_website

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

celery = Celery(
    "tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)


@celery.task
def scrape_quotes():
    logger.info("Starting scraping task")
    quotes = scrape_quotes_from_website()

    for quote in quotes:
        quote["date_added"] = datetime.utcnow()
        quotes_collection.insert_one(quote)
        logger.info(f"Saved quote by {quote['author']}")

    logger.info(f"Finished scraping, saved {len(quotes)} quotes")
    close_connection()
