from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from app.providers.base import DashboardProvider
from app.schemas.dashboard import Category, CustomsItem, ForecastDetailItem, ForecastSummaryItem, QueryChecklistItem


class SqliteDashboardProvider(DashboardProvider):
    def __init__(self, database_path: str) -> None:
        self.database_path = Path(database_path)

    def load_categories(self) -> list[Category]:
        rows = self._fetch_all("select * from categories order by phase, category")
        items: list[Category] = []
        for row in rows:
            items.append(
                Category(
                    phase=row["phase"],
                    category=row["category"],
                    targetYear=row["target_year"],
                    exportValue2024UsdBn=row["export_value_2024_usd_bn"],
                    exportValue2025UsdBn=row["export_value_2025_usd_bn"],
                    billingUnits2024M=row["billing_units_2024_m"],
                    billingUnits2025M=row["billing_units_2025_m"],
                    unitValueUsd=row["unit_value_usd"],
                    exporters2025=row["exporters_2025"],
                    priceBandRmb=json.loads(row["price_band_rmb"]),
                    growthAfter2026=row["growth_after_2026"],
                    source2024=row["source_2024"],
                    source2025=row["source_2025"],
                    note=row["note"],
                )
            )
        return items

    def load_forecast_summary(self, term: str) -> list[ForecastSummaryItem]:
        rows = self._fetch_all(
            "select * from forecast_summary where term = ? order by year, scenario",
            (term,),
        )
        return [
            ForecastSummaryItem(
                year=row["year"],
                scenario=row["scenario"],
                activeCategories=row["active_categories"],
                activeBillingUnitsM=row["active_billing_units_m"],
                activeExporters=row["active_exporters"],
                didPenetration=row["did_penetration"],
                codePenetration=row["code_penetration"],
                didRevenueM=row["did_revenue_m"],
                codeRevenueM=row["code_revenue_m"],
                consultingRevenueM=row["consulting_revenue_m"],
                totalRevenueM=row["total_revenue_m"],
            )
            for row in rows
        ]

    def load_forecast_detail(self) -> list[ForecastDetailItem]:
        rows = self._fetch_all("select * from forecast_detail order by year, scenario, category")
        return [
            ForecastDetailItem(
                year=row["year"],
                scenario=row["scenario"],
                category=row["category"],
                phase=row["phase"],
                launchFactor=row["launch_factor"],
                activeBillingUnitsM=row["active_billing_units_m"],
                activeExporters=row["active_exporters"],
                priceRmb=row["price_rmb"],
                penetration=row["penetration"],
                codeRevenueM=row["code_revenue_m"],
            )
            for row in rows
        ]

    def load_customs_items(self) -> list[CustomsItem]:
        rows = self._fetch_all("select * from customs_items order by category")
        return [
            CustomsItem(
                dataType=row["data_type"],
                category=row["category"],
                quantity2024=row["quantity_2024"],
                unit2024=row["unit_2024"],
                quantity2025=row["quantity_2025"],
                unit2025=row["unit_2025"],
                usableForDpp=row["usable_for_dpp"],
                note=row["note"],
            )
            for row in rows
        ]

    def load_query_checklist(self) -> list[QueryChecklistItem]:
        rows = self._fetch_all("select * from query_checklist order by priority, category")
        return [
            QueryChecklistItem(
                priority=row["priority"],
                category=row["category"],
                hasPublicQuantity=row["has_public_quantity"],
                queryDimensions=row["query_dimensions"],
                recommendedUnit=row["recommended_unit"],
                goal=row["goal"],
                note=row["note"],
            )
            for row in rows
        ]

    def _fetch_all(self, query: str, params: tuple = ()) -> list[sqlite3.Row]:
        if not self.database_path.exists():
            raise FileNotFoundError(
                f"SQLite dashboard database not found: {self.database_path}. "
                "Run backend/scripts/bootstrap_dashboard_db.py first."
            )
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            return list(connection.execute(query, params).fetchall())
        finally:
            connection.close()
