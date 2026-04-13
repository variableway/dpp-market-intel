# Task 1: DPP 数据采集 — 实施计划与任务拆解

## 总体目标

建立 DPP 市场情报数据的自动化采集管道，覆盖三大数据需求：
1. 分品类 DPP 申报数量统计
2. 2024/2025 对欧盟出口数据
3. 海关数据可用度和 HS 查询补拉

---

## Phase 1: UN Comtrade 数据采集管道（P1，最高优先级）

### Task 1.1: UN Comtrade API 接入

**目标：** 注册 UN Comtrade API，获取 subscription key，验证基本查询能力

**产出：**
- API key 配置到 `backend/.env`
- 验证脚本可成功查询中国对德出口数据

**步骤：**
1. 在 [comtradeplus.un.org](https://comtradeplus.un.org/) 注册账户
2. 在 [comtradedeveloper.un.org](https://comtradedeveloper.un.org/) 订阅免费计划获取 key
3. 测试 API 调用：中国（156）→ 德国（276），HS 章，2024 年出口
4. 将 key 存入 `backend/.env` 的 `UN_COMTRADE_API_KEY` 变量

**验收标准：** 能成功获取一条中国对欧盟国家的出口数据记录

**预计工作量：** 0.5 天

---

### Task 1.2: UN Comtrade Provider 实现

**目标：** 在后端 provider 架构中新增 `un_comtrade_provider`

**产出：**
- `backend/app/providers/dashboard/un_comtrade_provider.py`
- 在 factory.py 注册 `DASHBOARD_PROVIDER=un_comtrade`

**设计：**
```
class UnComtradeDashboardProvider(DashboardProvider):
    """从 UN Comtrade API 获取中国对 EU27 出口数据"""

    def __init__(self):
        self.api_key = os.getenv("UN_COMTRADE_API_KEY")
        self.cache_dir = Path("backend/data/cache/comtrade")

    def load_categories(self):
        # 查询 EU27 各国按 HS 章节的出口数据
        # 聚合为品类基线数据
        pass

    def load_customs_items(self):
        # 查询各 HS 章节的数量数据（如有）
        pass
```

**EU27 国家代码映射：**

| 国家 | Code | 国家 | Code |
|------|------|------|------|
| 奥地利 | 40 | 意大利 | 380 |
| 比利时 | 56 | 拉脱维亚 | 428 |
| 保加利亚 | 100 | 立陶宛 | 440 |
| 克罗地亚 | 191 | 卢森堡 | 442 |
| 塞浦路斯 | 196 | 马耳他 | 470 |
| 捷克 | 203 | 荷兰 | 528 |
| 丹麦 | 208 | 波兰 | 616 |
| 爱沙尼亚 | 233 | 葡萄牙 | 620 |
| 芬兰 | 246 | 罗马尼亚 | 642 |
| 法国 | 251 | 斯洛伐克 | 703 |
| 德国 | 276 | 斯洛文尼亚 | 705 |
| 希腊 | 300 | 西班牙 | 724 |
| 匈牙利 | 348 | 瑞典 | 752 |
| 爱尔兰 | 372 | | |

**HS 章节到 DPP 品类映射：**

| DPP 品类 | HS 章节 |
|---------|---------|
| 电池 | 8507 |
| 消费电子/电子电器 | 85 (减去 8507) |
| 纺织服装 | 50-63 |
| 轮胎/橡胶制品 | 40 |
| 钢铁及钢制品 | 72, 73 |
| 铝制品 | 76 |
| 家具 | 9401, 9403, 9405 |
| 床垫/寝具 | 9404 |
| 塑料/包装 | 39 |
| 涂料/洗涤剂 | 34 (部分) |
| 汽车及零部件 | 87 |
| 建筑材料 | 68, 69, 70 (部分) |
| 玩具 | 9503 |
| 化工/清洁剂/个人护理 | 33, 34 (部分) |
| 家电白电 | 8414, 8415, 8450, 8509 |
| 机械设备/工业装备 | 84 (部分), 85 (部分) |
| 纸张/木制品 | 47, 48, 44 |
| 医疗设备 | 9018, 9019, 9022 |
| 皮革/鞋类 | 41, 42, 64 |

**验收标准：** `DASHBOARD_PROVIDER=un_comtrade` 能返回与现有 CSV provider 相同 schema 的数据

**预计工作量：** 2-3 天

---

### Task 1.3: EU27 聚合查询脚本

**目标：** 编写批量查询 EU27 各国数据并聚合的脚本

**产出：**
- `backend/scripts/fetch_comtrade_eu27.py`

**功能：**
1. 循环查询 27 个欧盟成员国
2. 按 HS 章节聚合为中国对 EU27 整体出口数据
3. 输出为 `backend/data/csv/category_baseline_auto.csv`
4. 支持 dry-run 和缓存（避免重复 API 调用）

**命令行接口：**
```bash
cd backend
python3 scripts/fetch_comtrade_eu27.py \
  --year 2024 \
  --output data/csv/category_baseline_auto.csv \
  --cache-dir data/cache/comtrade
```

**验收标准：** 脚本可自动获取 2024 年中国对 EU27 出口金额，输出格式与现有 CSV 一致

**预计工作量：** 1-2 天

---

### Task 1.4: 数据缓存和增量更新

**目标：** 避免重复 API 调用，支持增量更新

**产出：**
- 缓存机制：将 API 响应缓存到 `backend/data/cache/comtrade/`
- 增量逻辑：只查询缓存中没有的年份/国家/HS 组合

**设计：**
```
data/cache/comtrade/
├── 2024/
│   ├── reporter_156_partner_276_cmd_AG2.json   # 中国→德国
│   ├── reporter_156_partner_246_cmd_AG2.json   # 中国→芬兰
│   └── ...
└── 2025/
    └── ...
```

**预计工作量：** 0.5-1 天

---

## Phase 2: 海关数量数据补拉（P1）

### Task 2.1: 海关 HS 查询自动化指南

**目标：** 为手动查询海关数据提供标准化操作流程

**产出：**
- `docs/customs-data-query-guide.md` — 海关互动查询操作手册
- 包含每个待补拉品类的具体查询步骤（HS 编码、国家选择、时间范围）

**查询步骤模板：**
1. 打开 http://stats.customs.gov.cn/
2. 选择"出口"
3. 币种选"美元"
4. 时间范围：2024-01 至 2024-12
5. 商品编码输入对应 HS 编码
6. 贸易伙伴选择欧盟各国
7. 导出结果

**待补拉品类清单（来自 eu_interactive_query_checklist.csv）：**

| 优先级 | 品类 | HS 查询维度 | 推荐单位 |
|-------|------|-----------|---------|
| P1 | 电池 | 8507 子目 | GWh/个 |
| P1 | 纺织服装 | 50-63 章 | 件/千克 |
| P1 | 轮胎/橡胶 | 40 章 (4011-4013) | 条/吨 |
| P1 | 钢铁 | 72-73 章 | 吨 |
| P1 | 铝制品 | 76 章 | 吨 |
| P1 | 消费电子 | 85 章 (8517, 8542 等) | 台/个 |
| P2 | 家具 | 9401, 9403 | 件/套 |
| P2 | 玩具 | 9503 | 件 |
| P2 | 纸张/木制品 | 47, 48, 44 章 | 件/吨 |
| P2 | 医疗设备 | 9018, 9019 | 台/件 |
| P3 | 塑料/包装 | 39 章 | 件/吨 |
| P3 | 化工/清洁剂 | 33, 34 章 (部分) | 件/升/千克 |

**预计工作量：** 0.5 天（文档编写）+ 持续手动查询

---

### Task 2.2: 海关数据录入脚本

**目标：** 将手动查询结果标准化录入系统

**产出：**
- `backend/scripts/import_customs_quantity.py` — 从手动导出的 CSV/Excel 导入海关数量数据
- 更新 `official_customs_quantity_extract_2024_2025.csv`

**验收标准：** 可将手动查询结果导入并更新 dashboard 数据

**预计工作量：** 0.5 天

---

## Phase 3: 数据刷新和静态导出集成（P2）

### Task 3.1: 数据刷新脚本

**目标：** 一键刷新所有数据源

**产出：**
- `backend/scripts/refresh_all_data.py` — 聚合所有数据采集步骤

**流程：**
```
refresh_all_data.py
  ├── 1. UN Comtrade API → category_baseline_auto.csv
  ├── 2. 海关缓存数据 → customs_quantity_updated.csv
  ├── 3. 数据聚合 → dashboard 聚合
  └── 4. export_static_data.py → frontend/public/data/*.json
```

**预计工作量：** 0.5 天

---

### Task 3.2: GitHub Actions 定时数据刷新

**目标：** 在 CI 中定期自动刷新数据

**产出：**
- 更新 `.github/workflows/deploy-pages.yml`
- 新增 `refresh-data` workflow（可手动触发或定期执行）

**设计：**
```yaml
name: Refresh Data
on:
  workflow_dispatch:  # 手动触发
  schedule:
    - cron: '0 3 1 */3 *'  # 每季度 1 号 UTC 3:00
jobs:
  refresh:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
      - name: Install deps
      - name: Fetch UN Comtrade data
        env:
          UN_COMTRADE_API_KEY: ${{ secrets.UN_COMTRADE_API_KEY }}
      - name: Export static JSON
      - name: Build frontend
      - name: Deploy
```

**预计工作量：** 0.5 天

---

### Task 3.3: 数据版本管理

**目标：** 追踪数据变更历史

**产出：**
- `data/CHANGELOG.md` — 记录每次数据更新的来源和时间
- 在 `dashboard.json` 的 meta 中增加 `dataSources` 字段

**预计工作量：** 0.5 天

---

## Phase 4: 辅助数据源集成（P3）

### Task 4.1: Eurostat Comext Provider（可选）

**目标：** 从 EU 视角交叉验证中国出口数据

**说明：** Eurostat 提供 EU 从中国进口的数据，可作为 UN Comtrade 中国报告出口的镜像验证。

**预计工作量：** 2 天

---

### Task 4.2: Trading Economics 数据验证（可选）

**目标：** 用 Trading Economics 数据验证 UN Comtrade 数据一致性

**说明：** 当前 CSV 数据来源为 Trading Economics，新数据需确保与之一致或能解释差异。

**预计工作量：** 1 天

---

### Task 4.3: EUR-Lex 法规跟踪（可选）

**目标：** 自动获取 ESPR/DPP 授权法案更新

**说明：** 通过 EUR-Lex SPARQL endpoint 或 RSS 跟踪 DPP 相关法规更新。

**预计工作量：** 2 天

---

## 任务总览和时间线

| Phase | Task | 优先级 | 预计工作量 | 依赖 |
|-------|------|--------|-----------|------|
| 1 | 1.1 UN Comtrade API 注册 | P1 | 0.5 天 | 无 |
| 1 | 1.2 Provider 实现 | P1 | 2-3 天 | 1.1 |
| 1 | 1.3 EU27 聚合脚本 | P1 | 1-2 天 | 1.2 |
| 1 | 1.4 缓存和增量更新 | P1 | 0.5-1 天 | 1.3 |
| 2 | 2.1 海关查询指南 | P1 | 0.5 天 | 无 |
| 2 | 2.2 海关数据录入脚本 | P1 | 0.5 天 | 无 |
| 3 | 3.1 数据刷新脚本 | P2 | 0.5 天 | 1.3, 2.2 |
| 3 | 3.2 GitHub Actions 定时刷新 | P2 | 0.5 天 | 3.1 |
| 3 | 3.3 数据版本管理 | P2 | 0.5 天 | 3.1 |
| 4 | 4.1 Eurostat Provider | P3 | 2 天 | 1.2 |
| 4 | 4.2 Trading Economics 验证 | P3 | 1 天 | 1.2 |
| 4 | 4.3 EUR-Lex 法规跟踪 | P3 | 2 天 | 无 |

**P1 总工作量：** 约 5-7 天
**P2 总工作量：** 约 1.5 天
**P3 总工作量：** 约 5 天

---

## 实施建议

1. **先做 Task 1.1** — 注册 API 并验证可行性
2. **再做 Task 1.2 + 1.3** — 核心自动化管道
3. **并行做 Task 2.1** — 海关查询指南
4. **完成 Phase 1 和 2 后进入 Phase 3** — 集成到现有构建流程
5. **Phase 4 按需排期** — 根据实际数据质量决定是否需要

## 文件结构（完成后新增）

```
backend/
├── .env                                    # UN_COMTRADE_API_KEY
├── data/
│   ├── cache/
│   │   └── comtrade/                       # API 响应缓存
│   │       └── {year}/
│   │           └── reporter_156_partner_{code}_cmd_AG2.json
│   └── csv/
│       └── category_baseline_auto.csv      # 自动采集的品类基线
├── scripts/
│   ├── fetch_comtrade_eu27.py              # EU27 聚合查询
│   ├── import_customs_quantity.py          # 海关数据录入
│   └── refresh_all_data.py                 # 一键刷新
├── app/providers/dashboard/
│   └── un_comtrade_provider.py             # UN Comtrade provider
docs/
└── customs-data-query-guide.md             # 海关查询操作手册
plan/
├── task1-feasibility-analysis.md           # 可行性分析
├── task1-implementation-plan.md            # 实施计划（本文件）
└── un-comtrade-api-research.md             # API 研究文档
```
