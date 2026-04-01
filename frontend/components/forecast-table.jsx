import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { formatNumber } from "@/lib/utils";

export function ForecastTable({ title, rows }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent className="overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead>
            <tr className="border-b border-border text-left text-muted-foreground">
              <th className="px-3 py-3">年份</th>
              <th className="px-3 py-3">场景</th>
              <th className="px-3 py-3">活跃品类</th>
              <th className="px-3 py-3">活跃计费单元(百万)</th>
              <th className="px-3 py-3">总营收(百万元)</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={`${row.year}-${row.scenario}`} className="border-b border-border/60 last:border-none">
                <td className="px-3 py-3 font-medium">{row.year}</td>
                <td className="px-3 py-3">{row.scenario}</td>
                <td className="px-3 py-3">{row.activeCategories}</td>
                <td className="px-3 py-3">{formatNumber(row.activeBillingUnitsM)}</td>
                <td className="px-3 py-3">{formatNumber(row.totalRevenueM)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </CardContent>
    </Card>
  );
}
