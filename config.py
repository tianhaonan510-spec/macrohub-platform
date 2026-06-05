from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_RAW = BASE_DIR / "data_raw"
DATA_CLEAN = BASE_DIR / "data_clean"
CACHE_DIR = BASE_DIR / "cache"
LOG_DIR = BASE_DIR / "logs"
METADATA_DIR = BASE_DIR / "metadata"
DB_PATH = DATA_CLEAN / "macrohub.db"

START_YEAR = 2015
END_YEAR = 2025

COUNTRIES = {
    "US": {"iso2": "US", "iso3": "USA", "zh": "美国", "en": "United States"},
    "CN": {"iso2": "CN", "iso3": "CHN", "zh": "中国", "en": "China"},
    "JP": {"iso2": "JP", "iso3": "JPN", "zh": "日本", "en": "Japan"},
    "DE": {"iso2": "DE", "iso3": "DEU", "zh": "德国", "en": "Germany"},
    "GB": {"iso2": "GB", "iso3": "GBR", "zh": "英国", "en": "United Kingdom"},
    "IN": {"iso2": "IN", "iso3": "IND", "zh": "印度", "en": "India"},
    "VN": {"iso2": "VN", "iso3": "VNM", "zh": "越南", "en": "Vietnam"},
    "ID": {"iso2": "ID", "iso3": "IDN", "zh": "印度尼西亚", "en": "Indonesia"},
    "MX": {"iso2": "MX", "iso3": "MEX", "zh": "墨西哥", "en": "Mexico"},
    "BR": {"iso2": "BR", "iso3": "BRA", "zh": "巴西", "en": "Brazil"},
    "ZA": {"iso2": "ZA", "iso3": "ZAF", "zh": "南非", "en": "South Africa"},
    "TR": {"iso2": "TR", "iso3": "TUR", "zh": "土耳其", "en": "Turkiye"},
    "AR": {"iso2": "AR", "iso3": "ARG", "zh": "阿根廷", "en": "Argentina"},
    "SA": {"iso2": "SA", "iso3": "SAU", "zh": "沙特阿拉伯", "en": "Saudi Arabia"},
}

IMF_WEO_MAPPING = {
    "NGDP_RPCH": "GDP_REAL_GROWTH_YOY_A",
    "PCPIPCH": "CPI_YOY_A",
    "LUR": "UNEMPLOYMENT_RATE_A",
    "GGXWDG_NGDP": "GOV_DEBT_GDP_A",
    "BCA_NGDPD": "CURRENT_ACCOUNT_GDP_A",
}

FRED_SERIES = {
    "US_CPI_INDEX_M": {
        "fred_series_id": "CPIAUCSL",
        "indicator_name_zh": "美国居民消费价格指数",
        "indicator_name_en": "U.S. Consumer Price Index",
        "unit": "index 1982-1984=100",
        "calculation": "level",
        "seasonal_adjustment": "SA",
    },
    "US_UNEMPLOYMENT_RATE_M": {
        "fred_series_id": "UNRATE",
        "indicator_name_zh": "美国失业率",
        "indicator_name_en": "U.S. Unemployment Rate",
        "unit": "%",
        "calculation": "level",
        "seasonal_adjustment": "SA",
    },
    "US_INDUSTRIAL_PRODUCTION_M": {
        "fred_series_id": "INDPRO",
        "indicator_name_zh": "美国工业生产指数",
        "indicator_name_en": "U.S. Industrial Production Index",
        "unit": "index 2017=100",
        "calculation": "level",
        "seasonal_adjustment": "SA",
    },
    "US_FED_FUNDS_RATE_M": {
        "fred_series_id": "FEDFUNDS",
        "indicator_name_zh": "美国联邦基金有效利率",
        "indicator_name_en": "U.S. Effective Federal Funds Rate",
        "unit": "%",
        "calculation": "level",
        "seasonal_adjustment": "NSA",
    },
}

INDICATOR_MAP = {
    "GDP_NOMINAL_USD_A": {
        "indicator_name_zh": "名义GDP",
        "indicator_name_en": "Nominal GDP",
        "unit": "current USD",
        "frequency": "A",
        "seasonal_adjustment": "NSA",
        "calculation": "level",
        "sources": [
            {"organization": "World Bank", "dataset": "World Development Indicators", "source_series_code": "NY.GDP.MKTP.CD"},
        ],
    },
    "GDP_REAL_GROWTH_YOY_A": {
        "indicator_name_zh": "实际GDP增速",
        "indicator_name_en": "Real GDP Growth",
        "unit": "%",
        "frequency": "A",
        "seasonal_adjustment": "NSA",
        "calculation": "YoY",
        "sources": [
            {"organization": "World Bank", "dataset": "World Development Indicators", "source_series_code": "NY.GDP.MKTP.KD.ZG"},
            {"organization": "IMF", "dataset": "World Economic Outlook", "source_series_code": "NGDP_RPCH"},
        ],
    },
    "GDP_PER_CAPITA_USD_A": {
        "indicator_name_zh": "人均GDP",
        "indicator_name_en": "GDP per capita",
        "unit": "current USD",
        "frequency": "A",
        "seasonal_adjustment": "NSA",
        "calculation": "level",
        "sources": [
            {"organization": "World Bank", "dataset": "World Development Indicators", "source_series_code": "NY.GDP.PCAP.CD"},
        ],
    },
    "CPI_YOY_A": {
        "indicator_name_zh": "居民消费价格指数同比",
        "indicator_name_en": "Consumer Price Index YoY",
        "unit": "%",
        "frequency": "A",
        "seasonal_adjustment": "NSA",
        "calculation": "YoY",
        "sources": [
            {"organization": "World Bank", "dataset": "World Development Indicators", "source_series_code": "FP.CPI.TOTL.ZG"},
            {"organization": "IMF", "dataset": "World Economic Outlook", "source_series_code": "PCPIPCH"},
        ],
    },
    "UNEMPLOYMENT_RATE_A": {
        "indicator_name_zh": "失业率",
        "indicator_name_en": "Unemployment Rate",
        "unit": "% of labor force",
        "frequency": "A",
        "seasonal_adjustment": "NSA",
        "calculation": "level",
        "sources": [
            {"organization": "World Bank", "dataset": "World Development Indicators", "source_series_code": "SL.UEM.TOTL.ZS"},
            {"organization": "IMF", "dataset": "World Economic Outlook", "source_series_code": "LUR"},
        ],
    },
    "EXPORTS_USD_A": {
        "indicator_name_zh": "货物和服务出口",
        "indicator_name_en": "Exports of goods and services",
        "unit": "current USD",
        "frequency": "A",
        "seasonal_adjustment": "NSA",
        "calculation": "level",
        "sources": [
            {"organization": "World Bank", "dataset": "World Development Indicators", "source_series_code": "NE.EXP.GNFS.CD"},
        ],
    },
    "IMPORTS_USD_A": {
        "indicator_name_zh": "货物和服务进口",
        "indicator_name_en": "Imports of goods and services",
        "unit": "current USD",
        "frequency": "A",
        "seasonal_adjustment": "NSA",
        "calculation": "level",
        "sources": [
            {"organization": "World Bank", "dataset": "World Development Indicators", "source_series_code": "NE.IMP.GNFS.CD"},
        ],
    },
    "RESERVES_USD_A": {
        "indicator_name_zh": "外汇储备",
        "indicator_name_en": "Total reserves",
        "unit": "current USD",
        "frequency": "A",
        "seasonal_adjustment": "NSA",
        "calculation": "level",
        "sources": [
            {"organization": "World Bank", "dataset": "World Development Indicators", "source_series_code": "FI.RES.TOTL.CD"},
        ],
    },
    "GOV_DEBT_GDP_A": {
        "indicator_name_zh": "政府债务占GDP比重",
        "indicator_name_en": "Central government debt, total",
        "unit": "% of GDP",
        "frequency": "A",
        "seasonal_adjustment": "NSA",
        "calculation": "level",
        "sources": [
            {"organization": "World Bank", "dataset": "World Development Indicators", "source_series_code": "GC.DOD.TOTL.GD.ZS"},
            {"organization": "IMF", "dataset": "World Economic Outlook", "source_series_code": "GGXWDG_NGDP"},
        ],
    },
    "CURRENT_ACCOUNT_GDP_A": {
        "indicator_name_zh": "经常账户余额占GDP比重",
        "indicator_name_en": "Current account balance",
        "unit": "% of GDP",
        "frequency": "A",
        "seasonal_adjustment": "NSA",
        "calculation": "level",
        "sources": [
            {"organization": "World Bank", "dataset": "World Development Indicators", "source_series_code": "BN.CAB.XOKA.GD.ZS"},
            {"organization": "IMF", "dataset": "World Economic Outlook", "source_series_code": "BCA_NGDPD"},
        ],
    },
}

for indicator_code, meta in FRED_SERIES.items():
    INDICATOR_MAP[indicator_code] = {
        "indicator_name_zh": meta["indicator_name_zh"],
        "indicator_name_en": meta["indicator_name_en"],
        "unit": meta["unit"],
        "frequency": "M",
        "seasonal_adjustment": meta["seasonal_adjustment"],
        "calculation": meta["calculation"],
        "sources": [
            {
                "organization": "FRED",
                "dataset": "Federal Reserve Economic Data",
                "source_series_code": meta["fred_series_id"],
            }
        ],
    }
