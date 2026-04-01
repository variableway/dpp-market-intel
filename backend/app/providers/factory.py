from __future__ import annotations

from app.core.config import Settings
from app.providers.base import DashboardProvider, NewsProvider
from app.providers.dashboard.csv_provider import CsvDashboardProvider
from app.providers.dashboard.sqlite_provider import SqliteDashboardProvider
from app.providers.news.json_seed_provider import JsonSeedNewsProvider
from app.providers.news.rss_provider import RssNewsProvider


class UnsupportedProviderError(ValueError):
    pass


def create_dashboard_provider(settings: Settings) -> DashboardProvider:
    if settings.dashboard_provider == "csv":
        return CsvDashboardProvider()
    if settings.dashboard_provider == "sqlite":
        return SqliteDashboardProvider(database_path=settings.dashboard_database_path)
    raise UnsupportedProviderError(
        f"Unsupported dashboard provider: {settings.dashboard_provider}. "
        "Currently supported: csv, sqlite"
    )


def create_news_provider(settings: Settings) -> NewsProvider:
    if settings.news_provider == "json_seed":
        return JsonSeedNewsProvider()
    if settings.news_provider == "rss":
        return RssNewsProvider(feeds=settings.news_rss_feeds)
    raise UnsupportedProviderError(
        f"Unsupported news provider: {settings.news_provider}. "
        "Currently supported: json_seed, rss"
    )
