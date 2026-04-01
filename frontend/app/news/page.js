import { AppShell } from "@/components/app-shell";
import { NewsFeed } from "@/components/news-feed";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { getNewsData } from "@/lib/api";

export default async function NewsPage() {
  const data = await getNewsData();

  return (
    <AppShell pathname="/news">
      <div className="mx-auto flex max-w-7xl flex-col gap-8 px-4 py-8 sm:px-6 lg:px-8">
        <section className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
          <Card className="overflow-hidden">
            <CardHeader className="bg-[linear-gradient(135deg,#082f49_0%,#155e75_50%,#fde68a_100%)] text-white">
              <div className="flex flex-wrap gap-2">
                <Badge variant="warm" className="bg-white/15 text-white">
                  Regulatory Pulse
                </Badge>
                <Badge variant="outline" className="border-white/40 bg-transparent text-white">
                  CBAM / DPP / Battery Passport
                </Badge>
              </div>
              <CardTitle className="mt-3 text-3xl">行业新闻与动态</CardTitle>
              <p className="max-w-2xl text-sm leading-7 text-white/85">
                这个页面面向业务推进和售前沟通。重点不是泛新闻，而是哪些政策动作会影响产品优先级、
                合规字段设计、客户教育节奏和重点行业销售顺序。
              </p>
            </CardHeader>
          </Card>

          <Card>
            <CardContent className="grid h-full gap-4 p-6">
              <div>
                <div className="text-sm text-muted-foreground">跟踪主题</div>
                <div className="mt-2 flex flex-wrap gap-2">
                  {data.topics.map((topic) => (
                    <Badge key={topic} variant="outline">
                      {topic}
                    </Badge>
                  ))}
                </div>
              </div>
              <div className="rounded-2xl bg-secondary p-4">
                <div className="text-sm font-medium">适合管理层看的三类信号</div>
                <ul className="mt-3 space-y-2 text-sm text-muted-foreground">
                  <li>法规是否进入明确生效和扩围阶段</li>
                  <li>是否出现新的服务商认证、数据管理、追溯规则</li>
                  <li>哪些品类会先变成销售和研发的高优先级</li>
                </ul>
              </div>
            </CardContent>
          </Card>
        </section>

        <NewsFeed topics={data.topics} items={data.items} />
      </div>
    </AppShell>
  );
}
