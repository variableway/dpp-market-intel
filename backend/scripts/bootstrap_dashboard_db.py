from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = ROOT / "backend"
DATA_DIR = BACKEND_ROOT / "data"
DATABASE_PATH = DATA_DIR / "dashboard.db"

if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.repositories.dashboard_repository import CsvDashboardRepository


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    repository = CsvDashboardRepository()

    connection = sqlite3.connect(DATABASE_PATH)
    try:
        cursor = connection.cursor()
        cursor.executescript(
            """
            drop table if exists categories;
            drop table if exists forecast_summary;
            drop table if exists forecast_detail;
            drop table if exists customs_items;
            drop table if exists query_checklist;

            create table categories (
              phase text not null,
              category text not null,
              target_year integer not null,
              export_value_2024_usd_bn real not null,
              export_value_2025_usd_bn real not null,
              billing_units_2024_m real not null,
              billing_units_2025_m real not null,
              unit_value_usd real not null,
              exporters_2025 integer not null,
              price_band_rmb text not null,
              growth_after_2026 real not null,
              source_2024 text not null,
              source_2025 text not null,
              note text not null
            );

            create table forecast_summary (
              term text not null,
              year integer not null,
              scenario text not null,
              active_categories integer not null,
              active_billing_units_m real not null,
              active_exporters real not null,
              did_penetration real not null,
              code_penetration real not null,
              did_revenue_m real not null,
              code_revenue_m real not null,
              consulting_revenue_m real not null,
              total_revenue_m real not null
            );

            create table forecast_detail (
              year integer not null,
              scenario text not null,
              category text not null,
              phase text not null,
              launch_factor real not null,
              active_billing_units_m real not null,
              active_exporters real not null,
              price_rmb real not null,
              penetration real not null,
              code_revenue_m real not null
            );

            create table customs_items (
              data_type text not null,
              category text not null,
              quantity_2024 real null,
              unit_2024 text not null,
              quantity_2025 real null,
              unit_2025 text not null,
              usable_for_dpp text not null,
              note text not null
            );

            create table query_checklist (
              priority text not null,
              category text not null,
              has_public_quantity text not null,
              query_dimensions text not null,
              recommended_unit text not null,
              goal text not null,
              note text not null
            );
            """
        )

        cursor.executemany(
            """
            insert into categories values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    item.phase,
                    item.category,
                    item.targetYear,
                    item.exportValue2024UsdBn,
                    item.exportValue2025UsdBn,
                    item.billingUnits2024M,
                    item.billingUnits2025M,
                    item.unitValueUsd,
                    item.exporters2025,
                    json.dumps(item.priceBandRmb.model_dump() if hasattr(item.priceBandRmb, "model_dump") else item.priceBandRmb),
                    item.growthAfter2026,
                    item.source2024,
                    item.source2025,
                    item.note,
                )
                for item in repository.load_categories()
            ],
        )

        forecast_rows = []
        for term in ("short", "long"):
            for item in repository.load_forecast_summary(term):
                forecast_rows.append(
                    (
                        term,
                        item.year,
                        item.scenario,
                        item.activeCategories,
                        item.activeBillingUnitsM,
                        item.activeExporters,
                        item.didPenetration,
                        item.codePenetration,
                        item.didRevenueM,
                        item.codeRevenueM,
                        item.consultingRevenueM,
                        item.totalRevenueM,
                    )
                )
        cursor.executemany("insert into forecast_summary values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", forecast_rows)

        cursor.executemany(
            "insert into forecast_detail values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                (
                    item.year,
                    item.scenario,
                    item.category,
                    item.phase,
                    item.launchFactor,
                    item.activeBillingUnitsM,
                    item.activeExporters,
                    item.priceRmb,
                    item.penetration,
                    item.codeRevenueM,
                )
                for item in repository.load_forecast_detail()
            ],
        )

        cursor.executemany(
            "insert into customs_items values (?, ?, ?, ?, ?, ?, ?, ?)",
            [
                (
                    item.dataType,
                    item.category,
                    item.quantity2024,
                    item.unit2024,
                    item.quantity2025,
                    item.unit2025,
                    item.usableForDpp,
                    item.note,
                )
                for item in repository.load_customs_items()
            ],
        )

        cursor.executemany(
            "insert into query_checklist values (?, ?, ?, ?, ?, ?, ?)",
            [
                (
                    item.priority,
                    item.category,
                    item.hasPublicQuantity,
                    item.queryDimensions,
                    item.recommendedUnit,
                    item.goal,
                    item.note,
                )
                for item in repository.load_query_checklist()
            ],
        )
        connection.commit()
        print(DATABASE_PATH)
    finally:
        connection.close()


if __name__ == "__main__":
    main()
