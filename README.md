# DPP Market Intel

一个完全独立的新目录项目，面向 DPP / CBAM 场景，提供：

- 分品类 Dashboard
- CBAM / DPP / Battery Passport 新闻流
- 可静态部署的网站产物
- 可切换 provider 的 FastAPI 数据后端

当前默认交付方式是**静态站优先**：

- 前端构建时直接读取 JSON
- 默认产物是可直接部署的静态文件
- 后端负责数据聚合、静态导出和未来动态 API

## 功能

1. 展现需 DPP 申报数据的数量分品类 Dashboard
2. 展现 CBAM / DPP / Battery Passport 相关行业新闻和动态
3. 聚合现有 DPP 业务测算、海关数量和 HS 查询缺口
4. 支持静态导出与 GitHub Pages / GitCode Pages 部署
5. 支持 provider 抽象，便于未来切换 CSV、数据库、远程 API、RSS 或爬虫来源

## 目录

```text
dpp-market-intel/
├── .github/workflows/       # GitHub Pages 自动部署
├── AGENTS.md                # 项目协作说明
├── backend/
│   ├── app/
│   ├── scripts/
│   ├── main.py
│   ├── news_seed.json
│   ├── requirements.txt
│   └── README.md
├── docs/
│   ├── README.md
│   ├── api-spec.md
│   ├── json-structure.md
│   └── provider-strategy.md
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── public/data/
│   ├── package.json
│   └── README.md
└── README.md
```

## 快速开始

### 1. 安装后端依赖

```bash
cd dpp-market-intel/backend
python3 -m pip install -r requirements.txt
```

### 2. 生成静态 JSON

```bash
cd dpp-market-intel/backend
python3 scripts/export_static_data.py
```

### 3. 安装前端依赖

```bash
cd dpp-market-intel/frontend
pnpm install
```

### 4. 本地开发

```bash
cd dpp-market-intel/frontend
pnpm dev
```

### 5. 静态构建

```bash
cd dpp-market-intel/frontend
pnpm build
```

静态输出目录为 `frontend/out`。

## 部署

### GitHub Pages

项目已提供：

- `.github/workflows/deploy-pages.yml`

推送到 `main` 后会自动：

1. 安装 backend / frontend 依赖
2. 导出静态 JSON
3. 构建静态站
4. 发布 `frontend/out`

### GitCode Pages

将 `frontend/out` 作为静态发布目录即可。

## Provider

后端当前采用 provider 工厂模式：

- `DASHBOARD_PROVIDER=csv`
- `NEWS_PROVIDER=json_seed`

当前已实现：

- Dashboard: CSV provider
- Dashboard: SQLite provider
- News: JSON seed provider
- News: RSS provider

未来可以继续增加：

- Dashboard: database / remote_api
- News: rss / crawler / cms

前提是不破坏文档里定义的 JSON schema。

## Provider 切换示例

### SQLite Dashboard

```bash
cd dpp-market-intel/backend
python3 scripts/bootstrap_dashboard_db.py
export DASHBOARD_PROVIDER=sqlite
export DASHBOARD_DATABASE_PATH=data/dashboard.db
python3 run.py
```

### RSS News

```bash
cd dpp-market-intel/backend
export NEWS_PROVIDER=rss
export NEWS_RSS_FEEDS=https://example.com/feed.xml
python3 run.py
```

## 文档

- [AGENTS.md](/Users/patrick/workspace/cew-biz/dpp-market-intel/AGENTS.md)
- [docs/README.md](/Users/patrick/workspace/cew-biz/dpp-market-intel/docs/README.md)
- [docs/api-spec.md](/Users/patrick/workspace/cew-biz/dpp-market-intel/docs/api-spec.md)
- [docs/json-structure.md](/Users/patrick/workspace/cew-biz/dpp-market-intel/docs/json-structure.md)
- [docs/provider-strategy.md](/Users/patrick/workspace/cew-biz/dpp-market-intel/docs/provider-strategy.md)
- [docs/strict-assessment-report.md](/Users/patrick/workspace/cew-biz/dpp-market-intel/docs/strict-assessment-report.md)
- [docs/minimal-upgrade-checklist.md](/Users/patrick/workspace/cew-biz/dpp-market-intel/docs/minimal-upgrade-checklist.md)
