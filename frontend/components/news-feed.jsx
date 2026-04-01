"use client";

import { useDeferredValue, useState } from "react";
import { ExternalLink, Search } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { formatDate } from "@/lib/utils";

export function NewsFeed({ topics, items }) {
  const [activeTopic, setActiveTopic] = useState("全部");
  const [query, setQuery] = useState("");
  const deferredQuery = useDeferredValue(query);

  const filtered = items.filter((item) => {
    const topicMatch = activeTopic === "全部" || item.topics.includes(activeTopic);
    const q = deferredQuery.trim().toLowerCase();
    const searchMatch =
      !q ||
      item.title.toLowerCase().includes(q) ||
      item.summary.toLowerCase().includes(q) ||
      item.impact.toLowerCase().includes(q);

    return topicMatch && searchMatch;
  });

  const featured = filtered[0];

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>过滤与检索</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="relative">
            <Search className="pointer-events-none absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <input
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="搜索政策、品类、法规动作"
              className="w-full rounded-full border border-border bg-white/80 py-3 pl-10 pr-4 text-sm outline-none ring-0"
            />
          </div>
          <div className="flex flex-wrap gap-2">
            {["全部", ...topics].map((topic) => (
              <Button
                key={topic}
                type="button"
                variant={activeTopic === topic ? "default" : "secondary"}
                onClick={() => setActiveTopic(topic)}
              >
                {topic}
              </Button>
            ))}
          </div>
        </CardContent>
      </Card>

      {featured ? (
        <Card className="overflow-hidden">
          <div className="bg-primary px-6 py-2 text-xs uppercase tracking-[0.3em] text-primary-foreground">
            Featured Update
          </div>
          <CardHeader>
            <div className="flex flex-wrap gap-2">
              {featured.topics.map((topic) => (
                <Badge key={topic} variant="warm">
                  {topic}
                </Badge>
              ))}
            </div>
            <CardTitle className="text-2xl">{featured.title}</CardTitle>
            <p className="text-sm text-muted-foreground">
              {featured.source} · {formatDate(featured.publishedAt)}
            </p>
          </CardHeader>
          <CardContent className="space-y-3">
            <p>{featured.summary}</p>
            <p className="text-sm text-muted-foreground">业务影响：{featured.impact}</p>
            <a
              href={featured.url}
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center gap-2 text-sm font-medium text-primary"
            >
              查看来源
              <ExternalLink className="h-4 w-4" />
            </a>
          </CardContent>
        </Card>
      ) : null}

      <div className="grid gap-4">
        {filtered.map((item) => (
          <Card key={item.id}>
            <CardContent className="p-6">
              <div className="flex flex-wrap items-center gap-2">
                {item.topics.map((topic) => (
                  <Badge key={`${item.id}-${topic}`} variant="outline">
                    {topic}
                  </Badge>
                ))}
              </div>
              <div className="mt-3 flex flex-col gap-3 lg:flex-row lg:items-start lg:justify-between">
                <div className="space-y-2">
                  <h3 className="text-xl font-semibold">{item.title}</h3>
                  <p className="text-sm text-muted-foreground">
                    {item.source} · {formatDate(item.publishedAt)} · {item.region}
                  </p>
                  <p className="text-sm leading-7">{item.summary}</p>
                  <p className="text-sm text-muted-foreground">业务影响：{item.impact}</p>
                </div>
                <a
                  href={item.url}
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center gap-2 text-sm font-medium text-primary"
                >
                  来源
                  <ExternalLink className="h-4 w-4" />
                </a>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
