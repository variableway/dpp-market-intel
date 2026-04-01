import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { formatCompact } from "@/lib/utils";

export function MetricCard({ label, value, unit, hint }) {
  return (
    <Card>
      <CardHeader className="pb-3">
        <CardTitle className="text-sm font-medium text-muted-foreground">{label}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex items-end gap-2">
          <div className="text-3xl font-semibold tracking-tight">{formatCompact(value)}</div>
          <div className="pb-1 text-sm text-muted-foreground">{unit}</div>
        </div>
        <p className="mt-3 text-sm text-muted-foreground">{hint}</p>
      </CardContent>
    </Card>
  );
}
