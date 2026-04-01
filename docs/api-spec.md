# API Spec

本项目前端默认使用静态 JSON 文件驱动，但 JSON 结构本身就是未来前后端接口的标准契约。也就是说：

- 静态部署时，页面直接读取 `frontend/public/data/*.json`
- 动态部署时，后端 API 应返回完全相同的 JSON 结构

## 1. Dashboard API

### 静态文件

- `frontend/public/data/dashboard.json`

### 对应 API

- `GET /api/dashboard`

### 参数

- 无

### 业务逻辑

- 聚合 DPP 品类基线数据
- 输出 KPI、阶段分布、分品类排行、收入预测、海关可用度和 HS 查询补拉清单
- 供首页 Dashboard 渲染使用

### JSON 结构

```json
{
  "meta": {
    "schema": "dashboard.v1",
    "updatedAt": "2026-04-01T00:00:00Z",
    "description": "Static dashboard payload for pure static deployment"
  },
  "data": {
    "updatedAt": "2026-04-01T00:00:00Z",
    "kpis": {
      "totalExportValue2025UsdBn": 450.29,
      "totalBillingUnits2025M": 16393.3,
      "totalExporters2025": 136300,
      "directCustomsCategories": 4,
      "partialCustomsCategories": 2,
      "pendingHsQueries": 12
    },
    "stageBreakdown": [],
    "categories": [],
    "topCategoriesByBillingUnits": [],
    "topCategoriesByExportValue": [],
    "forecast2027To2029": [],
    "forecast2030To2034": [],
    "hotCategories2029": [],
    "customsReadiness": {
      "direct": 4,
      "partial": 2,
      "pending": 12
    },
    "customsSamples": [],
    "queryChecklist": []
  }
}
```

## 2. News API

### 静态文件

- `frontend/public/data/news.json`

### 对应 API

- `GET /api/news`

### 参数

- 当前静态版本无运行时参数
- 动态 API 预留：
  - `topic`: 主题过滤，例如 `CBAM`
  - `q`: 关键词搜索，例如 `battery`

### 业务逻辑

- 输出新闻主题列表和新闻条目
- 供前端 News 页面做客户端过滤、搜索和主题切换
- 新闻内容重点聚焦 CBAM、DPP、Battery Passport、ESPR 等监管动态

### JSON 结构

```json
{
  "meta": {
    "schema": "news.v1",
    "updatedAt": "2026-04-01T00:00:00Z",
    "description": "Static news payload for pure static deployment"
  },
  "data": {
    "updatedAt": "2026-04-01T00:00:00Z",
    "topics": ["CBAM", "DPP", "Battery Passport"],
    "items": [
      {
        "id": "cbam-example",
        "publishedAt": "2025-12-17",
        "source": "European Commission",
        "title": "示例标题",
        "summary": "示例摘要",
        "impact": "示例业务影响",
        "topics": ["CBAM", "Steel"],
        "region": "EU",
        "url": "https://example.com"
      }
    ]
  }
}
```
