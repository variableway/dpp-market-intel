"""UN Comtrade API-backed dashboard provider.

Uses cached API data (fetched by fetch_comtrade_eu27.py) for trade values.
Falls back to CSV for forecast, customs, and checklist data (model-derived / static).
"""
from __future__ import annotations

import json
from pathlib import Path

from app.core.config import get_settings
from app.data.transformers import split_price_band, to_float, to_percent
from app.repositories.dashboard_repository import CsvDashboardRepository
from app.schemas.dashboard import Category

BACKEND_ROOT = Path(__file__).resolve().parents[3]
CACHE_DIR = BACKEND_ROOT / "data" / "cache" / "comtrade"


# DPP category → HS chapter mapping (same as fetch script)
HS_CHAPTER_MAP: dict[str, list[str]] = {
    "电池": ["8507"],
    "消费电子/电子电器": ["85"],  # whole chapter, minus 8507 handled in code
    "纺织服装": ["61", "62"],
    "轮胎/橡胶制品": ["40"],
    "钢铁及钢制品": ["72", "73"],
    "铝制品": ["76"],
    "家具": ["9401", "9403"],
    "床垫/寝具": ["9404"],
    "塑料/包装": ["39"],
    "涂料/洗涤剂": ["34"],
    "汽车及零部件": ["87"],
    "建筑材料": ["68", "69", "70"],
    "玩具": ["9503"],
    "化工/清洁剂/个人护理": ["33", "34"],
    "家电白电": ["8414", "8415", "8450", "8509"],
    "机械设备/工业装备": ["84"],  # minus white goods
    "纸张/木制品": ["47", "48", "44"],
    "医疗设备": ["9018", "9019", "9022"],
    "皮革/鞋类": ["41", "42", "64"],
}


def _load_cached_totals(year: int) -> dict[str, float]:
    """Load aggregated HS chapter totals from cache files.

    Returns dict of HS chapter code → total USD value.
    """
    chapter_totals: dict[str, float] = {}
    year_dir = CACHE_DIR / str(year)

    if not year_dir.exists():
        return {}

    for cache_file in sorted(year_dir.glob("partner_*_cmd_AG2_flow_X.json")):
        try:
            data = json.loads(cache_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue

        for rec in data.get("records", []):
            cmd = rec.get("cmdCode", "")
            value = rec.get("primaryValue", 0) or 0
            if cmd and value:
                chapter_totals[cmd] = chapter_totals.get(cmd, 0) + value

    return chapter_totals


class UnComtradeDashboardProvider:
    """Dashboard provider that uses UN Comtrade cached data for trade values.

    - Categories: trade values from cached API data, other fields from CSV baseline
    - Forecast, customs, checklist: from CSV (model-derived / static)
    """

    def __init__(self) -> None:
        self._csv_repo = CsvDashboardRepository()

    def load_categories(self) -> list[Category]:
        # Start with CSV baseline (has all fields)
        csv_categories = self._csv_repo.load_categories()

        # Try to enrich with cached API data
        totals_2024 = _load_cached_totals(2024)
        totals_2025 = _load_cached_totals(2025)

        if not totals_2024 and not totals_2025:
            return csv_categories

        for cat in csv_categories:
            chapters = HS_CHAPTER_MAP.get(cat.category, [])
            if not chapters:
                continue

            val_2024 = sum(totals_2024.get(ch, 0) for ch in chapters)
            val_2025 = sum(totals_2025.get(ch, 0) for ch in chapters)

            # Subtract excluded sub-chapters
            if cat.category == "消费电子/电子电器":
                val_2024 -= totals_2024.get("8507", 0)
                val_2025 -= totals_2025.get("8507", 0)
            elif cat.category == "机械设备/工业装备":
                for exc in ["8414", "8415", "8450", "8509"]:
                    val_2024 -= totals_2024.get(exc, 0)
                    val_2025 -= totals_2025.get(exc, 0)

            # Update only if we have meaningful data
            if val_2024 > 0:
                cat.exportValue2024UsdBn = round(val_2024 / 1e9, 2)
                cat.source2024 = f"UN Comtrade API ({', '.join(chapters)})"
            if val_2025 > 0:
                cat.exportValue2025UsdBn = round(val_2025 / 1e9, 2)
                cat.source2025 = f"UN Comtrade API ({', '.join(chapters)})"

        return csv_categories

    def load_forecast_summary(self, term: str) -> list:
        return self._csv_repo.load_forecast_summary(term=term)

    def load_forecast_detail(self) -> list:
        return self._csv_repo.load_forecast_detail()

    def load_customs_items(self) -> list:
        return self._csv_repo.load_customs_items()

    def load_query_checklist(self) -> list:
        return self._csv_repo.load_query_checklist()
