import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export function QueryChecklist({ items }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>待补拉查询清单</CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {items.map((item) => (
          <div
            key={item.category}
            className="rounded-2xl border border-border/80 bg-white/65 p-4"
          >
            <div className="flex flex-wrap items-center gap-3">
              <Badge variant={item.priority === "P1" ? "default" : "outline"}>{item.priority}</Badge>
              <div className="font-medium">{item.category}</div>
            </div>
            <div className="mt-3 text-sm text-muted-foreground">{item.queryDimensions}</div>
            <div className="mt-2 text-sm">推荐数量单位：{item.recommendedUnit}</div>
            <div className="mt-1 text-sm">目标：{item.goal}</div>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}
