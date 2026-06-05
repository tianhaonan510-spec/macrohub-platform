# MacroHub 全球宏观经济指标数据要素服务平台

MacroHub 面向“全球宏观经济指标数据要素采集与结构化服务”赛题，提供权威数据源接入、指标标准化治理、质量校验、SQLite 入库、CLI/FastAPI 查询和 Streamlit 可视化展示。

## 赛题能力对应

| 赛题要求 | 当前实现 |
| --- | --- |
| 多个权威宏观数据源 | World Bank Indicators API、IMF WEO 本地公开数据、FRED 月频公开数据 |
| 统一指标命名和维度描述 | `metadata/indicator_master.csv`、`metadata/source_mapping.csv`、`metadata/country_master.csv` |
| 按国家/指标/频率/时间查询 | CLI、`GET /query`、`POST /batch_query` |
| 标准化 JSON 输出 | 单条查询和批量查询均输出 JSON |
| 来源、单位、频率、季调、更新时间 | `macro_observations.csv` 中保留完整元数据 |
| 数据质量验证 | 总览、覆盖率、多来源一致性、异常值报告 |
| 缓存、重试、日志 | World Bank/FRED 本地缓存，requests retry，`logs/collect.log` |

## 数据源和覆盖

- World Bank: 年频跨国宏观指标，包括 GDP、CPI、失业率、贸易、外储、政府债务、经常账户等。
- IMF WEO: 年频跨国宏观指标，补充 GDP 增速、CPI、失业率、政府债务、经常账户等多来源校验。
- FRED: 美国月频指标，包括 CPI 指数、失业率、工业生产指数、联邦基金有效利率。

默认覆盖 14 个国家/地区、10 个年频标准指标，并扩展 4 个美国月频指标。

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

指定来源：

```bash
python query_cli.py --country US --indicator CPI_YOY_A --start 2020 --end 2024 --frequency A --source IMF
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
    {"country": "US", "indicator": "US_UNEMPLOYMENT_RATE_M", "start": "2024-01", "end": "2024-12", "frequency": "M", "source": "FRED"}
  ]
}
```

## Streamlit 展示

```bash
streamlit run dashboard/streamlit_app.py
```

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
- World Bank 和 FRED 在线采集依赖外部网络；无网络时可使用已有缓存和已生成的标准化数据。
- 当前修订追踪为轻量版本，保留 `last_updated`、`retrieved_at`、`data_version` 和采集批次 manifest，尚未保存每次历史修订快照。
