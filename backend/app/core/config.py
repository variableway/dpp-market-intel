from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True)
class Settings:
    app_name: str = "DPP Market Intel Backend"
    app_version: str = "0.2.0"
    api_prefix: str = "/api"
    cors_origins: tuple[str, ...] = ("*",)
    dashboard_provider: str = "csv"
    news_provider: str = "json_seed"
    dashboard_database_path: str = "data/dashboard.db"
    news_rss_feeds: tuple[str, ...] = ()


@lru_cache
def get_settings() -> Settings:
    raw_origins = os.getenv("CORS_ORIGINS")
    dashboard_provider = os.getenv("DASHBOARD_PROVIDER", "csv").strip() or "csv"
    news_provider = os.getenv("NEWS_PROVIDER", "json_seed").strip() or "json_seed"
    dashboard_database_path = os.getenv("DASHBOARD_DATABASE_PATH", "data/dashboard.db").strip() or "data/dashboard.db"
    raw_news_rss_feeds = os.getenv("NEWS_RSS_FEEDS", "")
    news_rss_feeds = tuple(item.strip() for item in raw_news_rss_feeds.split(",") if item.strip())
    if raw_origins:
        origins = tuple(item.strip() for item in raw_origins.split(",") if item.strip())
        return Settings(
            cors_origins=origins or ("*",),
            dashboard_provider=dashboard_provider,
            news_provider=news_provider,
            dashboard_database_path=dashboard_database_path,
            news_rss_feeds=news_rss_feeds,
        )
    return Settings(
        dashboard_provider=dashboard_provider,
        news_provider=news_provider,
        dashboard_database_path=dashboard_database_path,
        news_rss_feeds=news_rss_feeds,
    )
