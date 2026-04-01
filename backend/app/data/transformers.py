from __future__ import annotations


def to_float(value: str) -> float:
    return float(value.replace(",", "").strip())


def to_percent(value: str) -> float:
    return float(value.strip().replace("%", "")) / 100.0


def split_price_band(value: str) -> tuple[float, float, float]:
    low, mid, high = value.split("/")
    return float(low), float(mid), float(high)
