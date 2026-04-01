from __future__ import annotations

from typing import Protocol

from app.schemas.dashboard import Category, CustomsItem, ForecastDetailItem, ForecastSummaryItem, QueryChecklistItem
from app.schemas.news import NewsItem


class DashboardProvider(Protocol):
    def load_categories(self) -> list[Category]: ...

    def load_forecast_summary(self, term: str) -> list[ForecastSummaryItem]: ...

    def load_forecast_detail(self) -> list[ForecastDetailItem]: ...

    def load_customs_items(self) -> list[CustomsItem]: ...

    def load_query_checklist(self) -> list[QueryChecklistItem]: ...


class NewsProvider(Protocol):
    def list_items(self) -> list[NewsItem]: ...
