from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "frontend" / "public" / "data"
BACKEND_ROOT = ROOT / "backend"

if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.api.deps import get_dashboard_service, get_news_service


def dump_json(name: str, payload: dict) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / name
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    dashboard = get_dashboard_service().get_dashboard().model_dump(mode="json")
    news = get_news_service().get_news().model_dump(mode="json")

    dump_json(
        "dashboard.json",
        {
            "meta": {
                "schema": "dashboard.v1",
                "updatedAt": dashboard["updatedAt"],
                "description": "Static dashboard payload for pure static deployment",
            },
            "data": dashboard,
        },
    )
    dump_json(
        "news.json",
        {
            "meta": {
                "schema": "news.v1",
                "updatedAt": news["updatedAt"],
                "description": "Static news payload for pure static deployment",
            },
            "data": news,
        },
    )


if __name__ == "__main__":
    main()
