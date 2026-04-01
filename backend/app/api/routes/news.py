from fastapi import APIRouter, Depends, Query

from app.api.deps import get_news_service
from app.schemas.news import NewsResponse
from app.services.news_service import NewsService


router = APIRouter()


@router.get("/news", response_model=NewsResponse)
def get_news(
    topic: str | None = Query(default=None),
    q: str | None = Query(default=None),
    service: NewsService = Depends(get_news_service),
) -> NewsResponse:
    return service.get_news(topic=topic, query=q)
