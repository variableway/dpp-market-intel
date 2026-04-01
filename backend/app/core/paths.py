from __future__ import annotations

from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parents[2]
CSV_DATA_DIR = BACKEND_ROOT / "data" / "csv"

BASELINE_PATH = CSV_DATA_DIR / "category_baseline.csv"
FORECAST_SHORT_PATH = CSV_DATA_DIR / "forecast_2027_2029_summary.csv"
FORECAST_DETAIL_PATH = CSV_DATA_DIR / "forecast_2027_2029_detail.csv"
FORECAST_LONG_PATH = CSV_DATA_DIR / "forecast_2030_2034_summary.csv"
CUSTOMS_PATH = CSV_DATA_DIR / "official_customs_quantity_extract_2024_2025.csv"
CHECKLIST_PATH = CSV_DATA_DIR / "eu_interactive_query_checklist.csv"
NEWS_PATH = BACKEND_ROOT / "news_seed.json"
