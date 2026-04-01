import Link from "next/link";

import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

const links = [
  { href: "/", label: "Dashboard" },
  { href: "/news", label: "News" }
];

export function AppShell({ pathname, children }) {
  return (
    <div className="min-h-screen">
      <header className="sticky top-0 z-30 border-b border-white/50 bg-background/75 backdrop-blur-xl">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
          <div className="space-y-1">
            <div className="flex items-center gap-3">
              <Badge variant="warm">DPP + CBAM</Badge>
              <span className="text-xs uppercase tracking-[0.24em] text-muted-foreground">
                Market Intelligence
              </span>
            </div>
            <div className="text-lg font-semibold">跨境合规数据仪表盘</div>
          </div>
          <nav className="flex items-center gap-2 rounded-full border border-border/80 bg-white/70 p-1">
            {links.map((link) => {
              const active = pathname === link.href;
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  className={cn(
                    "rounded-full px-4 py-2 text-sm font-medium transition-colors",
                    active ? "bg-primary text-primary-foreground" : "text-muted-foreground hover:text-foreground"
                  )}
                >
                  {link.label}
                </Link>
              );
            })}
          </nav>
        </div>
      </header>
      <main className="data-grid">{children}</main>
    </div>
  );
}
