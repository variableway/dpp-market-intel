import { CircleAlert, DatabaseZap, FileSearch2 } from "lucide-react";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const icons = {
  direct: DatabaseZap,
  partial: FileSearch2,
  pending: CircleAlert
};

export function ReadinessPanel({ readiness }) {
  const items = [
    { key: "direct", label: "公开数量可直接用于 DPP", value: readiness.direct },
    { key: "partial", label: "公开数量部分可用", value: readiness.partial },
    { key: "pending", label: "仍需海关互动查询补拉", value: readiness.pending }
  ];

  return (
    <Card>
      <CardHeader>
        <CardTitle>海关与 HS 数据就绪度</CardTitle>
      </CardHeader>
      <CardContent className="grid gap-4 md:grid-cols-3">
        {items.map((item) => {
          const Icon = icons[item.key];
          return (
            <div key={item.key} className="rounded-2xl border border-border/80 bg-white/70 p-4">
              <div className="flex items-center justify-between">
                <div className="text-sm text-muted-foreground">{item.label}</div>
                <Icon className="h-5 w-5 text-primary" />
              </div>
              <div className="mt-4 text-3xl font-semibold">{item.value}</div>
            </div>
          );
        })}
      </CardContent>
    </Card>
  );
}
