# from typing import Optional
# from fastapi import FastAPI, Query
# from fastapi.middleware.cors import CORSMiddleware
# from storage.database import query_observations
# from config import DB_PATH
#
# app = FastAPI(title="MacroHub 全球宏观经济指标数据要素服务", version="1.0.0")
# app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
#
# @app.get("/")
# def home():
#     return {
#         "name": "MacroHub",
#         "description": "全球宏观经济指标数据要素采集与结构化服务",
#         "db_exists": DB_PATH.exists(),
#         "query_example": "/query?country=US&indicator=CPI_YOY_A&start=2015&end=2024&frequency=A"
#     }
#
# @app.get("/query")
# def query_macro(
#     country: str = Query(..., description="国家/地区代码，例如 US、CN"),
#     indicator: str = Query(..., description="标准指标编码，例如 CPI_YOY_A"),
#     start: Optional[str] = Query(None, description="开始时间，例如 2015"),
#     end: Optional[str] = Query(None, description="结束时间，例如 2024"),
#     frequency: Optional[str] = Query(None, description="频率：D/W/M/Q/A")
# ):
#     try:
#         df = query_observations(country, indicator, start, end, frequency)
#         request_obj = {"country": country, "indicator_code": indicator, "start_date": start, "end_date": end, "frequency": frequency}
#         if df.empty:
#             return {"request": request_obj, "series": None, "error": {"message": "No data found"}}
#         first = df.iloc[0].to_dict()
#         observations = []
#         for _, row in df.iterrows():
#             val = row.get("value")
#             observations.append({"date": str(row.get("date")), "value": None if val != val else float(val), "status": row.get("status") or "final"})
#         series = {
#             "series_id": first.get("series_id"),
#             "indicator_name_zh": first.get("indicator_name_zh"),
#             "indicator_name_en": first.get("indicator_name_en"),
#             "country_name_zh": first.get("country_name_zh"),
#             "country_name_en": first.get("country_name_en"),
#             "country_code": first.get("country_code"),
#             "frequency": first.get("frequency"),
#             "unit": first.get("unit"),
#             "seasonal_adjustment": first.get("seasonal_adjustment"),
#             "calculation": first.get("calculation"),
#             "source": {
#                 "organization": first.get("source_organization"),
#                 "dataset": first.get("source_dataset"),
#                 "source_series_code": first.get("source_indicator_code"),
#                 "source_url": first.get("source_url"),
#             },
#             "last_updated": first.get("last_updated"),
#             "observations": observations,
#         }
#         return {"request": request_obj, "series": series, "error": None}
#     except Exception as e:
#         return {"request": {"country": country, "indicator_code": indicator, "start_date": start, "end_date": end, "frequency": frequency}, "series": None, "error": {"message": str(e)}}




# -*- coding: utf-8 -*-
from typing import Optional

import sqlite3
import pandas as pd
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from config import DB_PATH


app = FastAPI(
    title="MacroHub 全球宏观经济指标数据要素服务",
    version="1.1.0",
    description="面向全球宏观经济指标的数据采集、标准化治理与 JSON API 服务"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def read_sql(query: str, params=None) -> pd.DataFrame:
    if params is None:
        params = []

    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(query, conn, params=params)


def query_observations_api(
    country: str,
    indicator: str,
    start: Optional[str] = None,
    end: Optional[str] = None,
    frequency: Optional[str] = None,
    source: Optional[str] = None
) -> pd.DataFrame:
    sql = """
        SELECT *
        FROM macro_observations
        WHERE country_code = ?
          AND indicator_code = ?
    """

    params = [country, indicator]

    if frequency:
        sql += " AND frequency = ?"
        params.append(frequency)

    if source:
        sql += " AND source_organization = ?"
        params.append(source)

    if start:
        sql += " AND CAST(date AS INTEGER) >= ?"
        params.append(int(start))

    if end:
        sql += " AND CAST(date AS INTEGER) <= ?"
        params.append(int(end))

    sql += " ORDER BY source_organization, CAST(date AS INTEGER)"

    return read_sql(sql, params)


@app.get("/")
def home():
    return {
        "name": "MacroHub",
        "description": "全球宏观经济指标数据要素采集、标准化治理与结构化服务平台",
        "version": "1.1.0",
        "db_path": str(DB_PATH),
        "db_exists": DB_PATH.exists(),
        "endpoints": {
            "query": "/query?country=US&indicator=CPI_YOY_A&start=2015&end=2024&frequency=A",
            "metadata": "/metadata",
            "health": "/health"
        }
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "db_exists": DB_PATH.exists()
    }


@app.get("/metadata")
def metadata():
    try:
        df = read_sql("SELECT * FROM macro_observations")

        return {
            "data_asset": {
                "table": "macro_observations",
                "rows": int(len(df)),
                "countries": int(df["country_code"].nunique()),
                "indicators": int(df["indicator_code"].nunique()),
                "sources": int(df["source_organization"].nunique())
            },
            "sources": sorted(df["source_organization"].dropna().unique().tolist()),
            "indicators": sorted(df["indicator_code"].dropna().unique().tolist()),
            "countries": sorted(df["country_code"].dropna().unique().tolist()),
            "error": None
        }

    except Exception as e:
        return {
            "data_asset": None,
            "sources": [],
            "indicators": [],
            "countries": [],
            "error": {"message": str(e)}
        }


@app.get("/query")
def query_macro(
    country: str = Query(..., description="国家/地区代码，例如 US、CN、AR"),
    indicator: str = Query(..., description="标准指标编码，例如 CPI_YOY_A"),
    start: Optional[str] = Query(None, description="开始时间，例如 2015"),
    end: Optional[str] = Query(None, description="结束时间，例如 2024"),
    frequency: Optional[str] = Query(None, description="频率代码，例如 A、Q、M"),
    source: Optional[str] = Query(None, description="数据来源，例如 IMF、World Bank")
):
    request_obj = {
        "country": country,
        "indicator_code": indicator,
        "start_date": start,
        "end_date": end,
        "frequency": frequency,
        "source": source
    }

    try:
        df = query_observations_api(
            country=country,
            indicator=indicator,
            start=start,
            end=end,
            frequency=frequency,
            source=source
        )

        if df.empty:
            return {
                "request": request_obj,
                "series": None,
                "error": {"message": "No data found"}
            }

        first = df.iloc[0].to_dict()

        observations = []
        for _, row in df.iterrows():
            val = row.get("value")

            observations.append({
                "date": str(row.get("date")),
                "value": None if pd.isna(val) else float(val),
                "status": row.get("status") or "final",
                "source_organization": row.get("source_organization")
            })

        series = {
            "series_id": first.get("series_id"),
            "indicator_code": first.get("indicator_code"),
            "indicator_name_zh": first.get("indicator_name_zh"),
            "indicator_name_en": first.get("indicator_name_en"),
            "country_name_zh": first.get("country_name_zh"),
            "country_name_en": first.get("country_name_en"),
            "country_code": first.get("country_code"),
            "frequency": first.get("frequency"),
            "unit": first.get("unit"),
            "seasonal_adjustment": first.get("seasonal_adjustment"),
            "calculation": first.get("calculation"),
            "source": {
                "organization": first.get("source_organization"),
                "dataset": first.get("source_dataset"),
                "source_series_code": first.get("source_indicator_code"),
                "source_url": first.get("source_url"),
            },
            "last_updated": first.get("last_updated"),
            "observations": observations,
        }

        return {
            "request": request_obj,
            "series": series,
            "error": None
        }

    except Exception as e:
        return {
            "request": request_obj,
            "series": None,
            "error": {"message": str(e)}
        }