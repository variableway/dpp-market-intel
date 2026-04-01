from __future__ import annotations

from functools import lru_cache

from app.core.config import get_settings
from app.providers.base import DashboardProvider, NewsProvider
from app.providers.factory import create_dashboard_provider, create_news_provider
from app.services.dashboard_service import DashboardService
from app.services.news_service import NewsService


@lru_cache
def get_dashboard_provider() -> DashboardProvider:
    return create_dashboard_provider(get_settings())


@lru_cache
def get_dashboard_service() -> DashboardService:
    return DashboardService(provider=get_dashboard_provider())


@lru_cache
def get_news_provider() -> NewsProvider:
    return create_news_provider(get_settings())


@lru_cache
def get_news_service() -> NewsService:
    return NewsService(provider=get_news_provider())
