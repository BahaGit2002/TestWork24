import logging
from typing import Optional

from fastapi import APIRouter, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings
from app.database import quotes_collection
from app.models import Quote
from app.schemas import TaskResponse
from app.tasks import scrape_quotes

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post("/parse-quotes-task", response_model=TaskResponse)
async def parse_quotes_task():
    logger.info("Starting quote scraping task")
    task = scrape_quotes.delay()
    return {"task_id": task.id}


@router.get("/quotes", response_model=list[Quote])
async def get_quotes(
    author: Optional[str] = None,
    tag: Optional[str] = None,
    limit: int = 10,
    skip: int = 0
):
    query = {}
    if author:
        query["author"] = author
    if tag:
        query["tags"] = {"$in": [tag]}

    quotes = list(quotes_collection.find(query).skip(skip).limit(limit))

    if not quotes:
        raise HTTPException(
            status_code=404,
            detail=f"No quotes found for author='{author}' and tag='{tag}'"
        )

    logger.info(
        f"Retrieved {len(quotes)} quotes with filters author={author}, tag={tag}"
    )
    return [Quote(**quote) for quote in quotes]
