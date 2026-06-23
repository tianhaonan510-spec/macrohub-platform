# MacroHub 全球宏观经济指标数据要素服务平台

MacroHub 面向“全球宏观经济指标数据要素采集与结构化服务”赛题，提供权威数据源接入、指标标准化治理、质量校验、SQLite 入库、CLI/FastAPI 查询和 Streamlit 可视化展示。

## 赛题能力对应

| 赛题要求 | 当前实现 |
| --- | --- |
| 多个权威宏观数据源 | World Bank、IMF WEO、FRED、OECD、Eurostat、ECB、BIS、中国国家统计局等 8 类来源，覆盖 55 个标准指标 |
| 统一指标命名和维度描述 | `metadata/indicator_master.csv`、`metadata/source_mapping.csv`、`metadata/country_master.csv` |
| 按国家/指标/频率/时间查询 | CLI、`GET /query`、`POST /batch_query` |
| 标准化 JSON 输出 | 单条查询和批量查询均输出 JSON |
| 来源、单位、频率、季调、更新时间 | `macro_observations.csv` 中保留完整元数据 |
| 数据质量验证 | 总览、覆盖率、多来源一致性、异常值报告 |
| 缓存、重试、日志 | 多个在线接口支持本地缓存与 requests retry，调度日志写入 `logs/` |

## 数据源和覆盖

- World Bank: 年频跨国宏观指标，包括 GDP、CPI、失业率、贸易、外储、政府债务、经常账户等。
- IMF WEO: 年频跨国宏观指标，补充 GDP 增速、CPI、失业率、政府债务、经常账户等多来源校验。
- FRED: 美国月频指标，包括 CPI 指数、失业率、工业生产指数、联邦基金有效利率。
- OECD: 月频 CPI 同比，覆盖 OECD 与部分 G20 经济体。
- Eurostat: 欧元区、德国、法国、意大利、西班牙 HICP 月频同比。
- ECB: 欧元兑美元日频参考汇率。
- BIS: 日频本币兑美元汇率，覆盖中国、美国、日本、欧元区及主要经济体。
- 中国国家统计局: 本地官方文件导入，当前包含中国 CPI、PPI、规模以上工业增加值等月度指标样例。

当前标准库覆盖 8 个数据源、18 个国家/地区、55 个标准指标，包含年频、月频和日频数据，共 60,824 条观测值；其中 19 个指标具备多源对齐关系，可用于跨机构口径比较和一致性校验。

## 安装

```bash
pip install -r requirements.txt
```

建议 Python 3.9+。如果 pandas 提示 `numexpr` 或 `bottleneck` 版本偏旧，可升级：

```bash
pip install -U numexpr bottleneck
```

## 一键采集、标准化、入库

```bash
python main_collect.py
```

常用参数：

```bash
python main_collect.py --force-refresh
python main_collect.py --skip-fred
python main_collect.py --fred-only
python main_collect.py --merge-only
```

生成文件：

- `data_raw/worldbank_raw.csv`
- `data_raw/imf/imf_standardized.csv`
- `data_raw/fred_raw.csv`
- `data_raw/oecd_raw.csv`
- `data_raw/eurostat_raw.csv`
- `data_raw/ecb_raw.csv`
- `data_raw/bis_raw.csv`
- `data_raw/china_official_raw.csv`
- `data_clean/macro_observations.csv`
- `data_clean/macrohub.db`
- `data_clean/quality_report.csv`
- `data_clean/quality_coverage_report.csv`
- `data_clean/quality_consistency_report.csv`
- `data_clean/quality_outlier_report.csv`
- `metadata/run_manifest.json`

## CLI 查询

单条查询：

```bash
python query_cli.py --country US --indicator CPI_YOY_A --start 2020 --end 2024 --frequency A
```

月频多来源 CPI 查询：

```bash
python query_cli.py --country DE --indicator CPI_YOY_M --start 2024-01 --end 2024-12 --frequency M
```

日频 BIS 中国汇率查询：

```bash
python query_cli.py --country CN --indicator EXCHANGE_RATE_USD_D --start 2024-01-02 --end 2024-01-10 --frequency D --source BIS
```

中国官方月频指标查询：

```bash
python query_cli.py --country CN --indicator CN_CPI_YOY_M --start 2024-01 --end 2024-12 --frequency M --source "National Bureau of Statistics of China"
```

20 条批量查询：

```bash
python query_cli.py --batch examples/sample_queries.json --output examples/sample_outputs.json
```

## FastAPI 服务

```bash
uvicorn api_service.app:app --reload
```

浏览器访问：

```text
http://127.0.0.1:8000/docs
```

单条查询：

```text
GET /query?country=US&indicator=CPI_YOY_A&start=2020&end=2024&frequency=A
```

批量查询：

```text
POST /batch_query
```

请求体示例：

```json
{
  "queries": [
    {"country": "US", "indicator": "CPI_YOY_A", "start": "2020", "end": "2024", "frequency": "A"},
    {"country": "US", "indicator": "US_UNEMPLOYMENT_RATE_M", "start": "2024-01", "end": "2024-12", "frequency": "M", "source": "FRED"},
    {"country": "DE", "indicator": "CPI_YOY_M", "start": "2024-01", "end": "2024-12", "frequency": "M"},
    {"country": "EA", "indicator": "EUR_USD_EXCHANGE_RATE_D", "start": "2024-01-02", "end": "2024-01-10", "frequency": "D", "source": "ECB"}
  ]
}
```

## 半自动指标对齐审核

平台采用“标准字典约束 + 智能候选推荐 + 置信评分 + 人工复核固化”的指标对齐机制。正式映射关系仍以 `metadata/source_mapping.csv` 为准，同时可通过脚本生成候选审核表：

```bash
python scripts/generate_alignment_candidates.py
```

脚本会读取 `metadata/indicator_master.csv`、`metadata/source_mapping.csv` 和 `data_clean/macro_observations.csv`，根据来源指标名称、原始代码、单位、频率及当前正式映射关系生成：

```text
metadata/alignment_candidates.csv
```

该文件包含候选标准指标、匹配得分、置信等级、推荐理由、审核状态、覆盖国家数和观测值规模。Streamlit 页面中的“指标对齐审核”模块可用于查看候选关系、筛选待复核项，并下载审核表。
## Streamlit 展示

```bash
streamlit run dashboard/streamlit_app.py
```


## 定时更新与调度

平台查询默认读取本地标准库 `data_clean/macrohub.db`，外部数据源通过采集任务定期刷新。推荐使用“固定时间自动采集 + 手动强制刷新”的模式，保证平台查询稳定、快速，同时保持数据可更新。

手动执行一次调度更新：

```bash
python scripts/scheduled_update.py
```

强制重新请求外部接口并更新本地库：

```bash
python scripts/scheduled_update.py --force-refresh
```

只验证调度状态文件，不改动数据：

```bash
python scripts/scheduled_update.py --dry-run
```

注册 Windows 每日定时任务，默认每天 02:00 运行：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/register_windows_task.ps1
```

指定每天 03:30 强制刷新：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/register_windows_task.ps1 -Time 03:30 -ForceRefresh
```

调度结果会写入 `metadata/update_status.json`，平台首页会显示最近更新时间、更新模式和调度状态。日志写入 `logs/scheduled_update.log`。
## JSON 输出说明

当查询结果只有一个来源时，`series` 为对象；当同一指标同时命中 IMF、World Bank 等多个来源时，`series` 为数组，每个来源保留独立的 `source` 和 `observations`，避免多来源数据混淆。

核心字段包括：

- `indicator_code`
- `country_code`
- `frequency`
- `unit`
- `seasonal_adjustment`
- `calculation`
- `source.organization`
- `source.dataset`
- `source.source_series_code`
- `last_updated`
- `observations[].date`
- `observations[].value`
- `observations[].status`

## 质量校验说明

`quality_report.csv` 提供总览指标；`quality_coverage_report.csv` 展示各指标和来源的覆盖情况；`quality_consistency_report.csv` 对多来源同国家、同指标、同日期的差异进行校验；`quality_outlier_report.csv` 使用 IQR 方法标记异常观测值。

## 已知边界

- IMF WEO 当前来自本地公开 CSV，需要先放入 `data_raw/imf/imf_weo.csv`。
- 中国国家统计局数据采用本地官方文件导入，示例文件位于 `data_raw/china_official/nbs_2024_monthly_sample.csv`。
- World Bank、FRED、OECD、Eurostat、ECB、BIS 在线采集依赖外部网络；无网络时可使用已有缓存和已生成的标准化数据。
- 当前修订追踪为轻量版本，保留 `last_updated`、`retrieved_at`、`data_version` 和采集批次 manifest，尚未保存每次历史修订快照。


