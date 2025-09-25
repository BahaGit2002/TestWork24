from datetime import datetime

from pydantic import BaseModel


class Quote(BaseModel):
    text: str
    author: str
    tags: list[str]
    date_added: datetime
