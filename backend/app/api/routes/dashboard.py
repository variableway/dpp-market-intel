from fastapi import APIRouter, Depends

from app.api.deps import get_dashboard_service
from app.schemas.dashboard import DashboardResponse
from app.services.dashboard_service import DashboardService


router = APIRouter()


@router.get("/dashboard", response_model=DashboardResponse)
def get_dashboard(
    service: DashboardService = Depends(get_dashboard_service),
) -> DashboardResponse:
    return service.get_dashboard()
