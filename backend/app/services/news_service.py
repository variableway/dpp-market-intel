from __future__ import annotations

from datetime import datetime, timezone

from app.providers.base import NewsProvider
from app.schemas.news import NewsResponse


class NewsService:
    def __init__(self, provider: NewsProvider) -> None:
        self.provider = provider

    def get_news(self, topic: str | None = None, query: str | None = None) -> NewsResponse:
        items = self.provider.list_items()

        if topic:
            items = [item for item in items if topic.lower() in [tag.lower() for tag in item.topics]]

        if query:
            lowered = query.lower()
            items = [
                item
                for item in items
                if lowered in item.title.lower()
                or lowered in item.summary.lower()
                or lowered in item.impact.lower()
            ]

        topics = sorted({topic_name for item in self.provider.list_items() for topic_name in item.topics})
        return NewsResponse(updatedAt=datetime.now(timezone.utc), topics=topics, items=items)
