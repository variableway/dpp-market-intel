from __future__ import annotations

from app.providers.base import NewsProvider
from app.repositories.news_repository import JsonNewsRepository


class JsonSeedNewsProvider(NewsProvider):
    def __init__(self) -> None:
        self.repository = JsonNewsRepository()

    def list_items(self):
        return self.repository.list_items()
