import { ArrowUpRight, Database, Newspaper, Radar } from "lucide-react";

import { AppShell } from "@/components/app-shell";
import { BarList } from "@/components/bar-list";
import { ForecastTable } from "@/components/forecast-table";
import { MetricCard } from "@/components/metric-card";
import { QueryChecklist } from "@/components/query-checklist";
import { ReadinessPanel } from "@/components/readiness-panel";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { getDashboardData } from "@/lib/api";
import { formatNumber } from "@/lib/utils";

export default async function DashboardPage() {
  const data = await getDashboardData();
  const { kpis } = data;

  return (
    <AppShell pathname="/">
      <div className="mx-auto flex max-w-7xl flex-col gap-8 px-4 py-8 sm:px-6 lg:px-8">
        <section className="grid gap-6 lg:grid-cols-[1.5fr_1fr]">
          <Card className="overflow-hidden">
            <div className="bg-[linear-gradient(135deg,#0f172a_0%,#0b5c7d_48%,#f97316_100%)] p-8 text-white">
              <Badge variant="warm" className="bg-white/15 text-white">
                新业务入口
              </Badge>
              <div className="mt-4 max-w-3xl text-4xl font-semibold tracking-tight">
                面向 DPP / CBAM 的跨境合规数据看板
              </div>
              <p className="mt-4 max-w-2xl text-sm leading-7 text-white/82">
                这个版本直接吃现有 DPP 测算、海关数量整理和政策追踪数据，帮助你同时看三件事：
                哪些品类量大、哪些品类已具备海关数据基础、哪些监管动态会改变平台产品路线。
              </p>
              <div className="mt-6 flex flex-wrap gap-4 text-sm text-white/90">
                <div className="flex items-center gap-2">
                  <Radar className="h-4 w-4" />
                  19 个 DPP 候选品类
                </div>
                <div className="flex items-center gap-2">
                  <Database className="h-4 w-4" />
                  海关数量+HS 查询缺口
                </div>
                <div className="flex items-center gap-2">
                  <Newspaper className="h-4 w-4" />
                  CBAM / DPP 政策新闻
                </div>
              </div>
            </div>
          </Card>

          <Card>
            <CardContent className="flex h-full flex-col justify-between p-6">
              <div>
                <div className="text-sm text-muted-foreground">2029 好场景</div>
                <div className="mt-2 text-4xl font-semibold text-primary">
                  {formatNumber(data.forecast2027To2029.at(-1).totalRevenueM)}
                </div>
                <div className="mt-1 text-sm text-muted-foreground">百万元总营收</div>
              </div>
              <div className="space-y-3 text-sm text-muted-foreground">
                {data.hotCategories2029.slice(0, 3).map((item) => (
                  <div key={item.category} className="flex items-center justify-between gap-4">
                    <div>{item.category}</div>
                    <div className="flex items-center gap-1 font-medium text-foreground">
                      {formatNumber(item.codeRevenueM)}
                      <ArrowUpRight className="h-4 w-4 text-accent" />
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </section>

        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          <MetricCard
            label="2025 对欧出口额"
            value={kpis.totalExportValue2025UsdBn}
            unit="USD bn"
            hint="扩充品类合计口径"
          />
          <MetricCard
            label="2025 DPP 计费单元"
            value={kpis.totalBillingUnits2025M}
            unit="百万"
            hint="适合一物一码追溯的合规单元"
          />
          <MetricCard
            label="2025 目标企业数"
            value={kpis.totalExporters2025}
            unit="家"
            hint="用于估算 DID 与企业覆盖"
          />
          <MetricCard
            label="可直接用于 DPP 的海关数量品类"
            value={kpis.directCustomsCategories}
            unit="类"
            hint="公开表已能直接用"
          />
          <MetricCard
            label="部分可用的海关数量品类"
            value={kpis.partialCustomsCategories}
            unit="类"
            hint="已有数量但仍需拆到欧盟口径"
          />
          <MetricCard
            label="待补拉 HS 查询"
            value={kpis.pendingHsQueries}
            unit="项"
            hint="适合做运营查询任务池"
          />
        </section>

        <section className="grid gap-6 xl:grid-cols-2">
          <BarList
            title="需 DPP 申报数据的数量分品类"
            description="按 2025 计费单元规模排序，直接反映一物一码的平台潜在吞吐量。"
            items={data.topCategoriesByBillingUnits}
            valueKey="billingUnits2025M"
            unit=" 百万"
          />
          <BarList
            title="分品类出口额"
            description="按 2025 对欧出口额排序，反映优先开拓的商业价值。"
            items={data.topCategoriesByExportValue}
            valueKey="exportValue2025UsdBn"
            unit=" USD bn"
            colorClass="bg-accent"
          />
        </section>

        <section className="grid gap-6 xl:grid-cols-[1.15fr_0.85fr]">
          <ForecastTable title="2027-2029 平台收入预测" rows={data.forecast2027To2029} />
          <ReadinessPanel readiness={data.customsReadiness} />
        </section>

        <section className="grid gap-6 xl:grid-cols-[0.95fr_1.05fr]">
          <QueryChecklist items={data.queryChecklist.slice(0, 8)} />
          <Card>
            <CardContent className="p-6">
              <div className="text-lg font-semibold">阶段分布</div>
              <p className="mt-2 text-sm text-muted-foreground">
                当前数据把 DPP 机会分成当前覆盖、近期纳入和中长期扩展三层，适合直接映射 roadmap。
              </p>
              <div className="mt-6 space-y-4">
                {data.stageBreakdown.map((item) => (
                  <div key={item.phase} className="rounded-2xl border border-border/80 bg-white/70 p-4">
                    <div className="flex items-center justify-between gap-4">
                      <div className="font-medium">{item.phase}</div>
                      <Badge variant="outline">{item.exporters2025} 家企业</Badge>
                    </div>
                    <div className="mt-4 grid gap-3 sm:grid-cols-2">
                      <div>
                        <div className="text-sm text-muted-foreground">2025 出口额</div>
                        <div className="mt-1 text-2xl font-semibold">{formatNumber(item.exportValue2025UsdBn)}</div>
                      </div>
                      <div>
                        <div className="text-sm text-muted-foreground">2025 计费单元(百万)</div>
                        <div className="mt-1 text-2xl font-semibold">{formatNumber(item.billingUnits2025M)}</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </section>
      </div>
    </AppShell>
  );
}
