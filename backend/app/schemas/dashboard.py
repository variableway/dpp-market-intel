from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class PriceBand(BaseModel):
    bad: float
    mid: float
    good: float


class Category(BaseModel):
    phase: str
    category: str
    targetYear: int
    exportValue2024UsdBn: float
    exportValue2025UsdBn: float
    billingUnits2024M: float
    billingUnits2025M: float
    unitValueUsd: float
    exporters2025: int
    priceBandRmb: PriceBand
    growthAfter2026: float
    source2024: str
    source2025: str
    note: str


class ForecastSummaryItem(BaseModel):
    year: int
    scenario: str
    activeCategories: int
    activeBillingUnitsM: float
    activeExporters: float
    didPenetration: float
    codePenetration: float
    didRevenueM: float
    codeRevenueM: float
    consultingRevenueM: float
    totalRevenueM: float


class ForecastDetailItem(BaseModel):
    year: int
    scenario: str
    category: str
    phase: str
    launchFactor: float
    activeBillingUnitsM: float
    activeExporters: float
    priceRmb: float
    penetration: float
    codeRevenueM: float


class CustomsItem(BaseModel):
    dataType: str
    category: str
    quantity2024: float | None
    unit2024: str
    quantity2025: float | None
    unit2025: str
    usableForDpp: str
    note: str


class QueryChecklistItem(BaseModel):
    priority: str
    category: str
    hasPublicQuantity: str
    queryDimensions: str
    recommendedUnit: str
    goal: str
    note: str


class PhaseBreakdown(BaseModel):
    phase: str
    exportValue2025UsdBn: float
    billingUnits2025M: float
    exporters2025: int


class DashboardKpis(BaseModel):
    totalExportValue2025UsdBn: float
    totalBillingUnits2025M: float
    totalExporters2025: int
    directCustomsCategories: int
    partialCustomsCategories: int
    pendingHsQueries: int


class CustomsReadiness(BaseModel):
    direct: int
    partial: int
    pending: int


class DashboardResponse(BaseModel):
    updatedAt: datetime
    kpis: DashboardKpis
    stageBreakdown: list[PhaseBreakdown]
    categories: list[Category]
    topCategoriesByBillingUnits: list[Category]
    topCategoriesByExportValue: list[Category]
    forecast2027To2029: list[ForecastSummaryItem]
    forecast2030To2034: list[ForecastSummaryItem]
    hotCategories2029: list[ForecastDetailItem]
    customsReadiness: CustomsReadiness
    customsSamples: list[CustomsItem]
    queryChecklist: list[QueryChecklistItem]
