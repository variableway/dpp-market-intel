from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone

from app.providers.base import DashboardProvider
from app.schemas.dashboard import DashboardKpis, DashboardResponse, PhaseBreakdown


class DashboardService:
    def __init__(self, provider: DashboardProvider) -> None:
        self.provider = provider

    def get_dashboard(self) -> DashboardResponse:
        categories = self.provider.load_categories()
        forecast_short = self.provider.load_forecast_summary(term="short")
        forecast_long = self.provider.load_forecast_summary(term="long")
        forecast_detail = self.provider.load_forecast_detail()
        customs_items = self.provider.load_customs_items()
        query_checklist = self.provider.load_query_checklist()

        direct_customs = sum(1 for item in customs_items if item.usableForDpp == "是")
        partial_customs = sum(1 for item in customs_items if item.usableForDpp == "部分可用")

        return DashboardResponse(
            updatedAt=datetime.now(timezone.utc),
            kpis=DashboardKpis(
                totalExportValue2025UsdBn=round(sum(item.exportValue2025UsdBn for item in categories), 2),
                totalBillingUnits2025M=round(sum(item.billingUnits2025M for item in categories), 2),
                totalExporters2025=sum(item.exporters2025 for item in categories),
                directCustomsCategories=direct_customs,
                partialCustomsCategories=partial_customs,
                pendingHsQueries=len(query_checklist),
            ),
            stageBreakdown=self._build_stage_breakdown(categories),
            categories=categories,
            topCategoriesByBillingUnits=sorted(
                categories, key=lambda item: item.billingUnits2025M, reverse=True
            )[:8],
            topCategoriesByExportValue=sorted(
                categories, key=lambda item: item.exportValue2025UsdBn, reverse=True
            )[:8],
            forecast2027To2029=forecast_short,
            forecast2030To2034=forecast_long,
            hotCategories2029=sorted(
                [item for item in forecast_detail if item.year == 2029],
                key=lambda item: item.codeRevenueM,
                reverse=True,
            )[:8],
            customsReadiness={
                "direct": direct_customs,
                "partial": partial_customs,
                "pending": len(query_checklist),
            },
            customsSamples=customs_items,
            queryChecklist=query_checklist,
        )

    def _build_stage_breakdown(self, categories: list) -> list[PhaseBreakdown]:
        grouped: dict[str, dict[str, float]] = defaultdict(
            lambda: {"exportValue2025UsdBn": 0.0, "billingUnits2025M": 0.0, "exporters2025": 0.0}
        )
        for item in categories:
            grouped[item.phase]["exportValue2025UsdBn"] += item.exportValue2025UsdBn
            grouped[item.phase]["billingUnits2025M"] += item.billingUnits2025M
            grouped[item.phase]["exporters2025"] += item.exporters2025

        return [
            PhaseBreakdown(
                phase=phase,
                exportValue2025UsdBn=round(values["exportValue2025UsdBn"], 2),
                billingUnits2025M=round(values["billingUnits2025M"], 2),
                exporters2025=int(values["exporters2025"]),
            )
            for phase, values in grouped.items()
        ]
