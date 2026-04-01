# JSON Structure

本项目把静态文件格式当成正式的数据契约。统一原则如下：

## 顶层结构

所有 JSON 文件统一采用两层包装：

```json
{
  "meta": {},
  "data": {}
}
```

含义：

- `meta`: 描述当前文件的 schema 版本、更新时间、用途说明
- `data`: 真正业务数据

## 设计理由

这样做有三个好处：

1. 静态文件和未来 API 响应可以完全共用一套格式。
2. 后续升级结构时，可以通过 `meta.schema` 做版本管理。
3. CDN、静态部署、后端接口、离线导出都可以共享同一份契约。

## dashboard.v1

`dashboard.json` 的 `data` 结构包含：

- `updatedAt`: 数据生成时间
- `kpis`: 首页核心指标
- `stageBreakdown`: 按阶段汇总
- `categories`: 全量品类基线数据
- `topCategoriesByBillingUnits`: 计费单元 Top 排行
- `topCategoriesByExportValue`: 出口额 Top 排行
- `forecast2027To2029`: 2027-2029 汇总预测
- `forecast2030To2034`: 2030-2034 汇总预测
- `hotCategories2029`: 2029 热点品类收入
- `customsReadiness`: 海关数据可用度
- `customsSamples`: 海关样本数据
- `queryChecklist`: 待补拉查询清单

## news.v1

`news.json` 的 `data` 结构包含：

- `updatedAt`: 数据生成时间
- `topics`: 所有可过滤主题
- `items`: 新闻列表

每条新闻包含：

- `id`
- `publishedAt`
- `source`
- `title`
- `summary`
- `impact`
- `topics`
- `region`
- `url`
