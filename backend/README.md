# Backend

已重构为 FastAPI 分层结构，核心原则是把 HTTP、业务聚合和数据获取分开，便于后续把 CSV/JSON 数据源替换为数据库、外部 API 或抓取任务。

## 结构

```text
backend/
├── app/
│   ├── api/           # 路由和依赖注入
│   ├── core/          # 配置与路径
│   ├── data/          # 通用文件加载与数据转换
│   ├── repositories/  # 数据访问层
│   ├── schemas/       # Pydantic 响应模型
│   └── services/      # 业务聚合层
├── main.py            # ASGI 入口
├── run.py             # 本地开发启动
├── news_seed.json
└── requirements.txt
```

## 设计说明

- `repositories` 负责“数据从哪里来”
- `services` 负责“数据怎么聚合成 dashboard/news”
- `api/routes` 负责“怎么暴露 HTTP 接口”
- `schemas` 负责响应契约，避免前后端字段漂移

这样后续如果新闻改成 RSS、数据库或第三方接口，只需要替换 `news_repository`，不用改 API 层。

## 安装

```bash
python3 -m pip install -r requirements.txt
```

## 启动

```bash
python3 run.py
```

或：

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

或：

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## API

- `GET /api/health`
- `GET /api/dashboard`
- `GET /api/news`
- `GET /api/news?topic=CBAM`
- `GET /api/news?q=battery`
