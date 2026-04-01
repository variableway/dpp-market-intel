from __future__ import annotations

from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = BACKEND_ROOT.parents[1]

BASELINE_PATH = REPO_ROOT / "dpp-new" / "output" / "category_baseline.csv"
FORECAST_SHORT_PATH = REPO_ROOT / "dpp-new" / "output" / "forecast_2027_2029_summary.csv"
FORECAST_DETAIL_PATH = REPO_ROOT / "dpp-new" / "output" / "forecast_2027_2029_detail.csv"
FORECAST_LONG_PATH = REPO_ROOT / "dpp-new" / "output" / "forecast_2030_2034_summary.csv"
CUSTOMS_PATH = REPO_ROOT / "dpp-customs" / "official_customs_quantity_extract_2024_2025.csv"
CHECKLIST_PATH = REPO_ROOT / "dpp-customs" / "eu_interactive_query_checklist.csv"
NEWS_PATH = BACKEND_ROOT / "news_seed.json"
