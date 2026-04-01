# Provider Strategy

前端静态化和后端可切换 provider 的思路是相通的，核心都是把“数据来源”和“页面/接口渲染”解耦。

## 1. 当前静态模式

当前模式是：

- 后端 service 聚合数据
- 导出脚本生成 `public/data/*.json`
- 前端构建时直接读取本地 JSON
- 构建产物输出为纯静态文件

这适合：

- GitHub Pages
- GitCode Pages
- 任意 CDN / Nginx 静态托管

## 2. 下一步可切换 provider

当前后端已经升级到 provider 工厂模式，使用环境变量选择数据来源：

- `DASHBOARD_PROVIDER=csv`
- `DASHBOARD_PROVIDER=sqlite`
- `NEWS_PROVIDER=json_seed`
- `NEWS_PROVIDER=rss`
- `DASHBOARD_DATABASE_PATH=backend/data/dashboard.db`
- `NEWS_RSS_FEEDS=https://example.com/feed.xml,https://example.com/feed2.xml`

建议数据 provider 按来源继续扩成以下几类：

### Dashboard Provider

- `csv_provider`
  - 读取现有仓库里的 CSV
- `database_provider`
  - 从 Postgres / MySQL 读结构化数据
- `remote_api_provider`
  - 从外部服务读取品类、海关和预测数据

### News Provider

- `json_seed_provider`
  - 读取手工维护的新闻 JSON
- `rss_provider`
  - 从指定 RSS 源抓新闻
- `crawler_provider`
  - 从官网页面抓取并清洗
- `editorial_provider`
  - 从 CMS 或后台录入系统读取

## 3. 推荐落地方式

无论后端未来切到哪种 provider，都建议保持两层输出：

1. 实时 API 输出
2. 静态导出 JSON 输出

这样可以同时支持：

- 静态站部署
- 动态站部署
- 内部后台或离线分析

## 4. 推荐接口约束

无论数据从哪里来，最终都应该输出统一 schema：

- `dashboard.v1`
- `news.v1`

只要 schema 不变，前端就不需要因为 provider 切换而改动。

## 5. 当前实现落点

当前代码已经具备以下结构：

- `app/providers/base.py`
  - 定义 provider 契约
- `app/providers/dashboard/csv_provider.py`
  - Dashboard CSV provider
- `app/providers/dashboard/sqlite_provider.py`
  - Dashboard SQLite provider
- `app/providers/news/json_seed_provider.py`
  - News JSON seed provider
- `app/providers/news/rss_provider.py`
  - News RSS provider
- `app/providers/factory.py`
  - 按配置选择 provider

下一步若接数据库或远程 API，只需要新增 provider 并在工厂中注册。
