# MacroHub 全球宏观经济指标数据要素服务平台

## 1. 安装依赖

```bash
pip install -r requirements.txt
```

## 2. 一键采集、标准化、质量检查、入库

```bash
python main_collect.py
```

生成文件：

```text
data_raw/worldbank_raw.csv
data_clean/macro_observations.csv
data_clean/macrohub.db
data_clean/quality_report.csv
metadata/indicator_master.csv
metadata/source_mapping.csv
metadata/country_master.csv
```

## 3. 命令行 JSON 查询

```bash
python query_cli.py --country US --indicator CPI_YOY_A --start 2015 --end 2024 --frequency A
```

## 4. 启动 FastAPI 服务

```bash
uvicorn api_service.app:app --reload
```

浏览器打开：

```text
http://127.0.0.1:8000/query?country=US&indicator=CPI_YOY_A&start=2015&end=2024&frequency=A
```

## 5. 启动平台界面

```bash
streamlit run dashboard/streamlit_app_1.py
```
