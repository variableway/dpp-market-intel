from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel


class NewsItem(BaseModel):
    id: str
    publishedAt: date
    source: str
    title: str
    summary: str
    impact: str
    topics: list[str]
    region: str
    url: str


class NewsResponse(BaseModel):
    updatedAt: datetime
    topics: list[str]
    items: list[NewsItem]
