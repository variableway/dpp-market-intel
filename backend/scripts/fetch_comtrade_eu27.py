"""
Fetch China-EU27 export data from UN Comtrade API.

Usage:
    cd backend
    python3 scripts/fetch_comtrade_eu27.py --year 2024
    python3 scripts/fetch_comtrade_eu27.py --year 2024 2025
    python3 scripts/fetch_comtrade_eu27.py --year 2024 --dry-run
    python3 scripts/fetch_comtrade_eu27.py --year 2024 --update-baseline

Requires UN_COMTRADE_API_KEY in backend/.env or environment.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BACKEND_ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = BACKEND_ROOT / "data" / "csv"
CACHE_DIR = BACKEND_ROOT / "data" / "cache" / "comtrade"
BASELINE_PATH = CSV_DIR / "category_baseline.csv"

# Load .env
try:
    from dotenv import load_dotenv
    load_dotenv(BACKEND_ROOT / ".env")
except ImportError:
    pass

# ---------------------------------------------------------------------------
# EU27 partner codes (M49)
# ---------------------------------------------------------------------------
EU27_CODES: dict[str, str] = {
    "40": "Austria", "56": "Belgium", "100": "Bulgaria", "191": "Croatia",
    "196": "Cyprus", "203": "Czechia", "208": "Denmark", "233": "Estonia",
    "246": "Finland", "251": "France", "276": "Germany", "300": "Greece",
    "348": "Hungary", "372": "Ireland", "380": "Italy", "428": "Latvia",
    "440": "Lithuania", "442": "Luxembourg", "470": "Malta", "528": "Netherlands",
    "616": "Poland", "620": "Portugal", "642": "Romania", "703": "Slovakia",
    "705": "Slovenia", "724": "Spain", "752": "Sweden",
}

# ---------------------------------------------------------------------------
# HS chapter(s) → DPP category mapping
# Each entry: (hs_chapters, category_name)
# Chapters are 2-digit strings used as cmdCode=AG2 filter values
# ---------------------------------------------------------------------------
HS_TO_CATEGORY: list[dict] = [
    {"chapters": ["85"], "category": "消费电子/电子电器",
     "note": "85 全章含电池，下面电池会单独扣减",
     "exclude_chapters": ["8507"]},
    {"chapters": ["8507"], "category": "电池",
     "note": "HS 8507 电池/蓄电池"},
    {"chapters": ["61", "62"], "category": "纺织服装",
     "note": "针织+非针织服装"},
    {"chapters": ["40"], "category": "轮胎/橡胶制品",
     "note": "橡胶及其制品"},
    {"chapters": ["72", "73"], "category": "钢铁及钢制品",
     "note": "钢铁+钢铁制品"},
    {"chapters": ["76"], "category": "铝制品",
     "note": "铝及其制品"},
    {"chapters": ["9401", "9403"], "category": "家具",
     "note": "座椅+其他家具"},
    {"chapters": ["9404"], "category": "床垫/寝具",
     "note": "床垫寝具"},
    {"chapters": ["39"], "category": "塑料/包装",
     "note": "塑料及其制品"},
    {"chapters": ["87"], "category": "汽车及零部件",
     "note": "车辆（非铁路）"},
    {"chapters": ["68", "69", "70"], "category": "建筑材料",
     "note": "玻璃陶瓷石材等建材"},
    {"chapters": ["9503"], "category": "玩具",
     "note": "玩具游戏品"},
    {"chapters": ["33", "34"], "category": "化工/清洁剂/个人护理",
     "note": "精油/化妆品/洗涤剂"},
    {"chapters": ["8414", "8415", "8450", "8509"], "category": "家电白电",
     "note": "制冷/空调/洗衣机/家电"},
    {"chapters": ["84"], "category": "机械设备/工业装备",
     "note": "机械设备（扣白电部分）",
     "exclude_chapters": ["8414", "8415", "8450", "8509"]},
    {"chapters": ["47", "48", "44"], "category": "纸张/木制品",
     "note": "纸浆/纸/木制品"},
    {"chapters": ["9018", "9019", "9022"], "category": "医疗设备",
     "note": "医疗器械"},
    {"chapters": ["41", "42", "64"], "category": "皮革/鞋类",
     "note": "皮革/箱包/鞋类"},
]

# For AG2 queries, chapters are 2-digit; for 4-digit headings we query separately
# We'll query at AG2 level for chapters and aggregate


# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------
API_BASE = "https://comtradeapi.un.org/data/v1/comtrade/final/get"


def _get_api_key() -> str:
    key = os.getenv("UN_COMTRADE_API_KEY", "").strip()
    if not key:
        print("ERROR: UN_COMTRADE_API_KEY not set. Add it to backend/.env")
        sys.exit(1)
    return key


def _fetch_cached(cache_path: Path) -> dict | None:
    if cache_path.exists():
        data = json.loads(cache_path.read_text(encoding="utf-8"))
        # Cache validity: 30 days
        cached_at = data.get("_cached_at", "")
        if cached_at:
            age = (datetime.now(timezone.utc) - datetime.fromisoformat(cached_at)).days
            if age < 30:
                return data
    return None


def _save_cache(cache_path: Path, data: dict) -> None:
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    data["_cached_at"] = datetime.now(timezone.utc).isoformat()
    cache_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def fetch_trade_data(
    api_key: str,
    year: int,
    partner_code: str,
    cmd_code: str = "AG2",
    flow_code: str = "X",
    use_cache: bool = True,
) -> list[dict]:
    """Fetch China exports to a partner country from UN Comtrade."""
    cache_path = CACHE_DIR / str(year) / f"partner_{partner_code}_cmd_{cmd_code}_flow_{flow_code}.json"

    if use_cache:
        cached = _fetch_cached(cache_path)
        if cached is not None:
            return cached.get("records", [])

    params = {
        "typeCode": "C",
        "freqCode": "A",
        "clCode": "HS",
        "period": str(year),
        "reporterCode": "156",  # China
        "partnerCode": partner_code,
        "cmdCode": cmd_code,
        "flowCode": flow_code,
        "maxRecords": "25000",
        "breakdownMode": "classic",
        "includeDesc": "true",
    }

    url = f"{API_BASE}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={
        "Ocp-Apim-Subscription-Key": api_key,
        "Accept": "application/json",
    })

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace") if e.fp else ""
        print(f"  HTTP {e.code} for partner={partner_code} cmd={cmd_code}: {error_body[:200]}")
        return []
    except Exception as e:
        print(f"  Error for partner={partner_code} cmd={cmd_code}: {e}")
        return []

    records = body.get("data", [])
    if use_cache and records:
        _save_cache(cache_path, {"records": records})

    return records


def fetch_all_eu27(
    api_key: str,
    year: int,
    cmd_code: str = "AG2",
    use_cache: bool = True,
    delay: float = 0.5,
) -> dict[str, float]:
    """Fetch China exports to all EU27 countries, aggregate by HS chapter.

    Returns: dict mapping HS 2-digit chapter code → total export value (USD)
    """
    chapter_totals: dict[str, float] = {}

    for code, name in EU27_CODES.items():
        print(f"  Fetching {year} → {name} ({code})...", end="", flush=True)
        records = fetch_trade_data(api_key, year, code, cmd_code=cmd_code, use_cache=use_cache)
        count = len(records)
        print(f" {count} records")

        for rec in records:
            cmd = rec.get("cmdCode", "")
            value = rec.get("primaryValue", 0) or 0
            if cmd and value:
                # For AG2, cmdCode is 2-digit HS chapter
                chapter_totals[cmd] = chapter_totals.get(cmd, 0) + value

        if delay > 0:
            time.sleep(delay)

    return chapter_totals


# ---------------------------------------------------------------------------
# Mapping: HS chapter totals → DPP category export values
# ---------------------------------------------------------------------------
def map_to_categories(
    totals_2024: dict[str, float],
    totals_2025: dict[str, float] | None,
) -> list[dict]:
    """Map HS chapter totals to DPP categories."""
    results = []

    # Also query at HS4 level for 4-digit headings
    # We'll aggregate what we can from AG2 and flag what needs HS4

    for mapping in HS_TO_CATEGORY:
        chapters = mapping["chapters"]
        exclude = set(mapping.get("exclude_chapters", []))

        val_2024 = 0.0
        val_2025 = 0.0

        for ch in chapters:
            val_2024 += totals_2024.get(ch, 0)
            if totals_2025 is not None:
                val_2025 += totals_2025.get(ch, 0)

        # Subtract excluded chapters
        for exc in exclude:
            val_2024 -= totals_2024.get(exc, 0)
            if totals_2025 is not None:
                val_2025 -= totals_2025.get(exc, 0)

        # Convert to billions USD
        val_2024_bn = round(val_2024 / 1e9, 2) if val_2024 else 0.0
        val_2025_bn = round(val_2025 / 1e9, 2) if val_2025 else 0.0

        results.append({
            "category": mapping["category"],
            "exportValue2024UsdBn": val_2024_bn,
            "exportValue2025UsdBn": val_2025_bn,
            "hsChapters": ", ".join(chapters),
            "excludeChapters": ", ".join(exclude) if exclude else "",
        })

    return results


# ---------------------------------------------------------------------------
# Merge with existing baseline CSV (preserve non-trade fields)
# ---------------------------------------------------------------------------
def merge_with_baseline(fetched: list[dict]) -> list[dict]:
    """Merge fetched trade values into existing baseline CSV."""
    # Read existing baseline
    existing: dict[str, dict] = {}
    if BASELINE_PATH.exists():
        with BASELINE_PATH.open("r", encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                existing[row["品类"]] = row

    # Build lookup by category name
    fetched_map = {item["category"]: item for item in fetched}

    # Update trade values in existing rows
    for cat_name, cat_row in existing.items():
        if cat_name in fetched_map:
            f = fetched_map[cat_name]
            if f["exportValue2024UsdBn"] > 0:
                cat_row["2024出口额(USD bn)"] = str(f["exportValue2024UsdBn"])
                cat_row["2024来源说明"] = f"UN Comtrade API 自动采集 ({f['hsChapters']})"
            if f["exportValue2025UsdBn"] > 0:
                cat_row["2025出口额(USD bn)"] = str(f["exportValue2025UsdBn"])
                cat_row["2025来源说明"] = f"UN Comtrade API 自动采集 ({f['hsChapters']})"

    return list(existing.values())


def write_baseline(rows: list[dict], path: Path) -> None:
    """Write rows back to CSV."""
    if not rows:
        return

    # Read original header order
    if BASELINE_PATH.exists():
        with BASELINE_PATH.open("r", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            header = next(reader)
    else:
        header = list(rows[0].keys())

    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch China-EU27 export data from UN Comtrade")
    parser.add_argument("--year", nargs="+", type=int, default=[2024],
                        help="Year(s) to fetch (default: 2024)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Fetch and display results without updating CSV")
    parser.add_argument("--update-baseline", action="store_true",
                        help="Merge fetched data into category_baseline.csv")
    parser.add_argument("--no-cache", action="store_true",
                        help="Ignore cache, force fresh API calls")
    parser.add_argument("--output", type=str, default=None,
                        help="Output CSV path (default: stdout)")
    args = parser.parse_args()

    api_key = _get_api_key()
    use_cache = not args.no_cache

    totals: dict[int, dict[str, float]] = {}

    for year in args.year:
        print(f"\n{'='*60}")
        print(f"Fetching {year} China → EU27 export data")
        print(f"{'='*60}")
        totals[year] = fetch_all_eu27(api_key, year, cmd_code="AG2", use_cache=use_cache)

    # Display summary
    print(f"\n{'='*60}")
    print("HS Chapter Totals (USD)")
    print(f"{'='*60}")
    for year in sorted(totals.keys()):
        print(f"\n--- {year} ---")
        for ch in sorted(totals[year].keys(), key=lambda x: totals[year][x], reverse=True):
            val_bn = totals[year][ch] / 1e9
            if val_bn >= 0.01:
                print(f"  HS {ch:>4s}: {val_bn:>10.2f} Bn USD")

    # Map to DPP categories
    t24 = totals.get(args.year[0], {})
    t25 = totals.get(args.year[1], {}) if len(args.year) > 1 else None
    fetched = map_to_categories(t24, t25)

    print(f"\n{'='*60}")
    print("DPP Category Mapping")
    print(f"{'='*60}")
    for item in fetched:
        line = f"  {item['category']:<20s} 2024: {item['exportValue2024UsdBn']:>8.2f} Bn"
        if item["exportValue2025UsdBn"] > 0:
            line += f"  2025: {item['exportValue2025UsdBn']:>8.2f} Bn"
        print(line)

    if args.update_baseline:
        merged = merge_with_baseline(fetched)
        output_path = Path(args.output) if args.output else BASELINE_PATH
        write_baseline(merged, output_path)
        print(f"\nUpdated baseline written to: {output_path}")
    elif args.output:
        # Write just the fetched mapping
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fetched[0].keys())
            writer.writeheader()
            writer.writerows(fetched)
        print(f"\nFetched data written to: {output_path}")
    else:
        print("\n(Dry run — no files updated. Use --update-baseline to merge into CSV)")


if __name__ == "__main__":
    main()
