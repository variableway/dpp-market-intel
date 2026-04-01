from __future__ import annotations

from app.core.paths import (
    BASELINE_PATH,
    CHECKLIST_PATH,
    CUSTOMS_PATH,
    FORECAST_DETAIL_PATH,
    FORECAST_LONG_PATH,
    FORECAST_SHORT_PATH,
)
from app.data.file_loaders import read_csv_rows
from app.data.transformers import split_price_band, to_float, to_percent
from app.schemas.dashboard import (
    Category,
    CustomsItem,
    ForecastDetailItem,
    ForecastSummaryItem,
    QueryChecklistItem,
)


class CsvDashboardRepository:
    def load_categories(self) -> list[Category]:
        categories: list[Category] = []
        for row in read_csv_rows(BASELINE_PATH):
            bad, mid, good = split_price_band(row["一码价格(坏/中/好,RMB)"])
            categories.append(
                Category(
                    phase=row["阶段"],
                    category=row["品类"],
                    targetYear=int(row["目标纳入年"]),
                    exportValue2024UsdBn=to_float(row["2024出口额(USD bn)"]),
                    exportValue2025UsdBn=to_float(row["2025出口额(USD bn)"]),
                    billingUnits2024M=to_float(row["2024计费单元(百万)"]),
                    billingUnits2025M=to_float(row["2025计费单元(百万)"]),
                    unitValueUsd=to_float(row["平均计费单元价值(USD)"]),
                    exporters2025=int(row["2025目标企业数"]),
                    priceBandRmb={"bad": bad, "mid": mid, "good": good},
                    growthAfter2026=to_percent(row["2026后年增长假设"]),
                    source2024=row["2024来源说明"],
                    source2025=row["2025来源说明"],
                    note=row["备注"],
                )
            )
        return categories

    def load_forecast_summary(self, term: str) -> list[ForecastSummaryItem]:
        path = FORECAST_SHORT_PATH if term == "short" else FORECAST_LONG_PATH
        items: list[ForecastSummaryItem] = []
        for row in read_csv_rows(path):
            items.append(
                ForecastSummaryItem(
                    year=int(row["年份"]),
                    scenario=row["场景"],
                    activeCategories=int(row["活跃品类数"]),
                    activeBillingUnitsM=to_float(row["活跃计费单元(百万)"]),
                    activeExporters=to_float(row["活跃企业数(去重后)"]),
                    didPenetration=to_percent(row["DID渗透率"]),
                    codePenetration=to_percent(row["一码渗透率"]),
                    didRevenueM=to_float(row["DID收入(百万元)"]),
                    codeRevenueM=to_float(row["一码收入(百万元)"]),
                    consultingRevenueM=to_float(row["Consulting收入(百万元)"]),
                    totalRevenueM=to_float(row["总营收(百万元)"]),
                )
            )
        return items

    def load_forecast_detail(self) -> list[ForecastDetailItem]:
        items: list[ForecastDetailItem] = []
        for row in read_csv_rows(FORECAST_DETAIL_PATH):
            items.append(
                ForecastDetailItem(
                    year=int(row["年份"]),
                    scenario=row["场景"],
                    category=row["品类"],
                    phase=row["阶段"],
                    launchFactor=to_float(row["启动系数"]),
                    activeBillingUnitsM=to_float(row["活跃计费单元(百万)"]),
                    activeExporters=to_float(row["活跃企业数"]),
                    priceRmb=to_float(row["一码单价(RMB)"]),
                    penetration=to_percent(row["一码渗透率"]),
                    codeRevenueM=to_float(row["一码收入(百万元)"]),
                )
            )
        return items

    def load_customs_items(self) -> list[CustomsItem]:
        items: list[CustomsItem] = []
        for row in read_csv_rows(CUSTOMS_PATH):
            items.append(
                CustomsItem(
                    dataType=row["数据类型"],
                    category=row["品类"],
                    quantity2024=None if row["2024数量"] == "-" else to_float(row["2024数量"]),
                    unit2024=row["2024单位"],
                    quantity2025=None if row["2025数量"] == "-" else to_float(row["2025数量"]),
                    unit2025=row["2025单位"],
                    usableForDpp=row["是否可直接用于DPP"],
                    note=row["说明"],
                )
            )
        return items

    def load_query_checklist(self) -> list[QueryChecklistItem]:
        items: list[QueryChecklistItem] = []
        for row in read_csv_rows(CHECKLIST_PATH):
            items.append(
                QueryChecklistItem(
                    priority=row["优先级"],
                    category=row["DPP品类"],
                    hasPublicQuantity=row["公开海关页面是否已有数量"],
                    queryDimensions=row["建议去海关查询页补拉的维度"],
                    recommendedUnit=row["建议优先数量单位"],
                    goal=row["查询目标"],
                    note=row["备注"],
                )
            )
        return items
