# -*- coding: utf-8 -*-
"""
IMF WEO 数据采集器
读取 data_raw/imf/imf_weo.csv，将 IMF WEO 宽表转换为平台标准长表。

运行方式：
python -m collectors.imf_collector
"""

from pathlib import Path
import pandas as pd

from config import DATA_RAW, COUNTRIES, INDICATOR_MAP

RAW_FILE = DATA_RAW / "imf" / "imf_weo.csv"
OUT_FILE = DATA_RAW / "imf" / "imf_standardized.csv"


# IMF WEO 中 SERIES_CODE 的第二段是指标代码，例如 USA.PCPIPCH.A
# PCPIPCH 对应 CPI 同比，NGDP_RPCH 对应实际 GDP 增速
IMF_WEO_MAPPING = {
    "NGDP_RPCH": "GDP_REAL_GROWTH_YOY_A",
    "PCPIPCH": "CPI_YOY_A",
    "LUR": "UNEMPLOYMENT_RATE_A",
    "GGXWDG_NGDP": "GOV_DEBT_GDP_A",
    "BCA_NGDPD": "CURRENT_ACCOUNT_GDP_A",
}


def clean_value(x):
    if pd.isna(x):
        return None

    text = str(x).strip().replace(",", "")

    if text in ["", "n/a", "N/A", "--", "nan", "NaN"]:
        return None

    try:
        return float(text)
    except Exception:
        return None


def extract_country_from_series(series_code):
    # USA.PCPIPCH.A -> USA
    try:
        return str(series_code).split(".")[0]
    except Exception:
        return None


def extract_indicator_from_series(series_code):
    # USA.PCPIPCH.A -> PCPIPCH
    try:
        parts = str(series_code).split(".")
        if len(parts) >= 2:
            return parts[1]
        return None
    except Exception:
        return None


def read_imf_weo():
    if not RAW_FILE.exists():
        raise FileNotFoundError(f"未找到 IMF 文件：{RAW_FILE}")

    df = pd.read_csv(RAW_FILE, encoding="utf-8-sig", low_memory=False)

    print("[IMF] 原始文件读取成功")
    print(f"[IMF] shape={df.shape}")
    print("[IMF] 字段预览：")
    print(df.columns[:30].tolist())

    return df


def transform_imf_weo(df):
    required_cols = ["SERIES_CODE", "COUNTRY", "INDICATOR", "FREQUENCY"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"IMF 文件缺少必要字段：{col}")

    # 提取 ISO3 和 IMF 指标代码
    df["imf_country_iso3"] = df["SERIES_CODE"].apply(extract_country_from_series)
    df["imf_indicator_code"] = df["SERIES_CODE"].apply(extract_indicator_from_series)

    # 只保留平台需要的 IMF 指标
    df = df[df["imf_indicator_code"].isin(IMF_WEO_MAPPING.keys())].copy()

    # 只保留当前平台配置中的国家
    iso3_to_platform = {
        info["iso3"]: code
        for code, info in COUNTRIES.items()
    }

    df["country_code"] = df["imf_country_iso3"].map(iso3_to_platform)
    df = df[df["country_code"].notna()].copy()

    # 年份列
    year_cols = [c for c in df.columns if str(c).isdigit()]

    rows = []

    for _, row in df.iterrows():
        platform_country = row["country_code"]
        country_info = COUNTRIES.get(platform_country, {})

        imf_indicator_code = row["imf_indicator_code"]
        indicator_code = IMF_WEO_MAPPING.get(imf_indicator_code)
        indicator_meta = INDICATOR_MAP.get(indicator_code, {})

        for year in year_cols:
            value = clean_value(row.get(year))

            rows.append({
                "series_id": f"{platform_country}.{indicator_code}.IMF",
                "country_code": platform_country,
                "country_iso2": country_info.get("iso2", platform_country),
                "country_iso3": country_info.get("iso3", row["imf_country_iso3"]),
                "country_name_zh": country_info.get("zh", ""),
                "country_name_en": country_info.get("en", row.get("COUNTRY", "")),
                "indicator_code": indicator_code,
                "indicator_name_zh": indicator_meta.get("indicator_name_zh", row.get("INDICATOR", "")),
                "indicator_name_en": indicator_meta.get("indicator_name_en", row.get("INDICATOR", "")),
                "date": str(year),
                "frequency": "A",
                "unit": indicator_meta.get("unit", row.get("UNIT", "")),
                "seasonal_adjustment": indicator_meta.get("seasonal_adjustment", "NSA"),
                "calculation": indicator_meta.get("calculation", ""),
                "value": value,
                "source_organization": "IMF",
                "source_dataset": "World Economic Outlook",
                "source_indicator_code": imf_indicator_code,
                "source_series_code": row.get("SERIES_CODE", ""),
                "source_indicator_name": row.get("INDICATOR", ""),
                "source_url": "https://data.imf.org/en/datasets/IMF.RES:WEO",
                "last_updated": row.get("UPDATE_DATE", ""),
                "status": "official",
            })

    out = pd.DataFrame(rows)

    # 限制到项目时间范围
    # 如果 config.py 中 START_YEAR/END_YEAR 后续要用，也可以加进去
    out = out.sort_values(["country_code", "indicator_code", "date"])

    return out


def main():
    df_raw = read_imf_weo()
    df_std = transform_imf_weo(df_raw)

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df_std.to_csv(OUT_FILE, index=False, encoding="utf-8-sig")

    print(f"[IMF] 标准化完成，rows={len(df_std)}")
    print(f"[IMF] saved: {OUT_FILE}")


if __name__ == "__main__":
    main()