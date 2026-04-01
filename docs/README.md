# DPP Market Intel Docs

## 项目功能

这是一个面向 DPP / CBAM 场景的市场情报与业务看板项目，当前包含两个核心页面：

- `Dashboard`
  - 展示需 DPP 申报数据的分品类数量统计
  - 展示收入预测、海关可用度、待补拉 HS 清单
- `News`
  - 展示 CBAM / DPP / Battery Passport 相关新闻和政策动态
  - 支持前端静态过滤和关键词搜索

## 当前使用方式

本项目当前默认是**纯静态部署模式**。

含义是：

- 前端不依赖运行中的后端接口
- 页面构建时直接读取本地 JSON 文件
- `next build` 直接输出静态站点
- 可直接部署到 GitHub Pages、GitCode Pages 或任意静态托管平台

## 关键目录

- `frontend/public/data/`
  - 静态数据文件
- `backend/scripts/export_static_data.py`
  - 从后端 service 导出静态 JSON 的脚本
- `docs/api-spec.md`
  - API 和静态 JSON 的正式契约说明
- `docs/json-structure.md`
  - JSON 顶层结构和字段设计说明
- `docs/provider-strategy.md`
  - 可切换 provider 的后续思路
- `docs/strict-assessment-report.md`
  - 当前版本的严格评估报告
- `docs/minimal-upgrade-checklist.md`
  - 从原型到准生产版的最小升级清单

## 如何生成静态数据

```bash
cd backend
python3 -m pip install -r requirements.txt
python3 scripts/export_static_data.py
```

执行后会生成：

- `frontend/public/data/dashboard.json`
- `frontend/public/data/news.json`

## 可选：初始化 SQLite Dashboard 数据源

```bash
cd backend
python3 scripts/bootstrap_dashboard_db.py
```

执行后会生成：

- `backend/data/dashboard.db`

然后可以通过环境变量切换 provider：

```bash
export DASHBOARD_PROVIDER=sqlite
export DASHBOARD_DATABASE_PATH=backend/data/dashboard.db
```

## 可选：启用 RSS News Provider

```bash
export NEWS_PROVIDER=rss
export NEWS_RSS_FEEDS=https://example.com/feed.xml,https://example.com/feed2.xml
```

## 如何构建静态站点

```bash
cd frontend
pnpm install
pnpm build
```

构建后默认输出目录为：

- `frontend/out`

这个目录可以直接部署。

## 推荐部署方式

### GitHub / GitCode Pages

把 `frontend/out` 作为发布目录即可。

### GitHub Pages 自动部署

项目已提供：

- `.github/workflows/deploy-pages.yml`

默认行为：

- 安装 backend / frontend 依赖
- 自动导出静态 JSON
- 执行静态构建
- 上传 `frontend/out` 到 GitHub Pages

如果站点不是根路径部署，而是仓库子路径部署，workflow 默认会把 `BASE_PATH` 设置为仓库名。

### GitCode Pages

当前项目没有绑定 GitCode 专用 CI 配置文件，但已经满足 GitCode Pages 的核心条件：

- 构建结果是纯静态 `frontend/out`
- 不依赖 Node/ Python 运行时

因此只需要把 `frontend/out` 作为发布目录即可。

### 任意静态服务器

将 `frontend/out` 上传到 Nginx、OSS、COS、CDN 或 Pages 服务即可。

## 为什么这套方式适合后续 provider 扩展

因为前端当前只认固定 JSON schema，不关心数据具体来自：

- CSV
- 数据库
- 外部 API
- RSS
- 爬虫
- CMS

这意味着未来只要保持 JSON 契约不变，就可以逐步把静态数据源替换为动态 provider，而不需要重写前端页面。
