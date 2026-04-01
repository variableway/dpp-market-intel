import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { formatNumber } from "@/lib/utils";

export function BarList({ title, description, items, valueKey, unit, colorClass = "bg-primary" }) {
  const max = Math.max(...items.map((item) => item[valueKey]), 1);

  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
        <p className="text-sm text-muted-foreground">{description}</p>
      </CardHeader>
      <CardContent className="space-y-4">
        {items.map((item) => (
          <div key={item.category} className="space-y-2">
            <div className="flex items-center justify-between gap-4 text-sm">
              <div className="font-medium">{item.category}</div>
              <div className="text-muted-foreground">
                {formatNumber(item[valueKey])}
                {unit}
              </div>
            </div>
            <div className="h-3 overflow-hidden rounded-full bg-muted">
              <div
                className={`h-full rounded-full ${colorClass}`}
                style={{ width: `${(item[valueKey] / max) * 100}%` }}
              />
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}
