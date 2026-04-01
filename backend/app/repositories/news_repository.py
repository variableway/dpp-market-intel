from __future__ import annotations

from app.core.paths import NEWS_PATH
from app.data.file_loaders import read_json
from app.schemas.news import NewsItem


class JsonNewsRepository:
    def list_items(self) -> list[NewsItem]:
        raw_items = read_json(NEWS_PATH)
        items = [NewsItem(**item) for item in raw_items]
        return sorted(items, key=lambda item: item.publishedAt, reverse=True)
