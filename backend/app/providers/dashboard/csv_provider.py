from __future__ import annotations

from app.providers.base import DashboardProvider
from app.repositories.dashboard_repository import CsvDashboardRepository


class CsvDashboardProvider(DashboardProvider):
    def __init__(self) -> None:
        self.repository = CsvDashboardRepository()

    def load_categories(self):
        return self.repository.load_categories()

    def load_forecast_summary(self, term: str):
        return self.repository.load_forecast_summary(term=term)

    def load_forecast_detail(self):
        return self.repository.load_forecast_detail()

    def load_customs_items(self):
        return self.repository.load_customs_items()

    def load_query_checklist(self):
        return self.repository.load_query_checklist()
