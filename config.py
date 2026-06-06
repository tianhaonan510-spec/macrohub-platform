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
    "FR": {"iso2": "FR", "iso3": "FRA", "zh": "法国", "en": "France"},
    "IT": {"iso2": "IT", "iso3": "ITA", "zh": "意大利", "en": "Italy"},
    "ES": {"iso2": "ES", "iso3": "ESP", "zh": "西班牙", "en": "Spain"},
    "EA": {"iso2": "EA", "iso3": "EA20", "zh": "欧元区", "en": "Euro area"},
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

OECD_SERIES = {
    "CPI_YOY_M": {
        "url": "https://sdmx.oecd.org/public/rest/v1/data/OECD.SDD.TPS,DSD_PRICES@DF_PRICES_ALL/.M.N.CPI.PA._T.N.GY?startPeriod=2015-01&dimensionAtObservation=AllDimensions",
        "indicator_name_zh": "居民消费价格指数同比",
        "indicator_name_en": "Consumer Price Index YoY",
        "unit": "%",
        "frequency": "M",
        "seasonal_adjustment": "NSA",
        "calculation": "YoY",
        "source_series_code": "DF_PRICES_ALL.CPI.GY",
    }
}

EUROSTAT_SERIES = {
    "CPI_YOY_M": {
        "dataset": "prc_hicp_manr",
        "params": {"coicop": "CP00"},
        "geos": ["EA20", "DE", "FR", "IT", "ES"],
        "indicator_name_zh": "调和居民消费价格指数同比",
        "indicator_name_en": "HICP annual rate of change",
        "unit": "%",
        "frequency": "M",
        "seasonal_adjustment": "NSA",
        "calculation": "YoY",
        "source_series_code": "prc_hicp_manr.CP00",
    }
}

ECB_SERIES = {
    "EUR_USD_EXCHANGE_RATE_D": {
        "flow": "EXR",
        "key": "D.USD.EUR.SP00.A",
        "indicator_name_zh": "欧元兑美元参考汇率",
        "indicator_name_en": "Euro foreign exchange reference rate: USD",
        "unit": "USD per EUR",
        "frequency": "D",
        "seasonal_adjustment": "NSA",
        "calculation": "level",
        "source_series_code": "EXR.D.USD.EUR.SP00.A",
    }
}

BIS_SERIES = {
    "EXCHANGE_RATE_USD_D": {
        "countries": ["CN", "US", "JP", "DE", "GB", "IN", "BR", "ZA", "TR", "MX", "EA"],
        "indicator_name_zh": "本币兑美元汇率",
        "indicator_name_en": "Exchange rates against USD",
        "unit": "local currency per USD",
        "frequency": "D",
        "seasonal_adjustment": "NSA",
        "calculation": "level",
        "source_series_code": "WS_XRU.D",
    }
}

CHINA_OFFICIAL_SERIES = {
    "CN_CPI_YOY_M": {
        "indicator_name_zh": "中国居民消费价格指数同比",
        "indicator_name_en": "China CPI YoY",
        "unit": "%",
        "frequency": "M",
        "seasonal_adjustment": "NSA",
        "calculation": "YoY",
        "source_series_code": "NBS.CPI.YOY.M",
        "source_dataset": "National Bureau of Statistics monthly data",
    },
    "CN_PPI_YOY_M": {
        "indicator_name_zh": "中国工业生产者出厂价格指数同比",
        "indicator_name_en": "China PPI YoY",
        "unit": "%",
        "frequency": "M",
        "seasonal_adjustment": "NSA",
        "calculation": "YoY",
        "source_series_code": "NBS.PPI.YOY.M",
        "source_dataset": "National Bureau of Statistics monthly data",
    },
    "CN_INDUSTRIAL_VALUE_ADDED_YOY_M": {
        "indicator_name_zh": "中国规模以上工业增加值同比",
        "indicator_name_en": "China industrial value added YoY",
        "unit": "%",
        "frequency": "M",
        "seasonal_adjustment": "NSA",
        "calculation": "YoY",
        "source_series_code": "NBS.IVA.YOY.M",
        "source_dataset": "National Bureau of Statistics monthly data",
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
    "CPI_YOY_M": {
        "indicator_name_zh": "居民消费价格指数同比",
        "indicator_name_en": "Consumer Price Index YoY",
        "unit": "%",
        "frequency": "M",
        "seasonal_adjustment": "NSA",
        "calculation": "YoY",
        "sources": [
            {"organization": "OECD", "dataset": "Prices: Consumer prices", "source_series_code": "DF_PRICES_ALL.CPI.GY"},
            {"organization": "Eurostat", "dataset": "HICP monthly annual rate of change", "source_series_code": "prc_hicp_manr.CP00"},
        ],
    },
    "EUR_USD_EXCHANGE_RATE_D": {
        "indicator_name_zh": "欧元兑美元参考汇率",
        "indicator_name_en": "Euro foreign exchange reference rate: USD",
        "unit": "USD per EUR",
        "frequency": "D",
        "seasonal_adjustment": "NSA",
        "calculation": "level",
        "sources": [
            {"organization": "ECB", "dataset": "Euro foreign exchange reference rates", "source_series_code": "EXR.D.USD.EUR.SP00.A"},
        ],
    },
    "EXCHANGE_RATE_USD_D": {
        "indicator_name_zh": "本币兑美元汇率",
        "indicator_name_en": "Exchange rates against USD",
        "unit": "local currency per USD",
        "frequency": "D",
        "seasonal_adjustment": "NSA",
        "calculation": "level",
        "sources": [
            {"organization": "BIS", "dataset": "Exchange rates", "source_series_code": "WS_XRU.D"},
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

for indicator_code, meta in CHINA_OFFICIAL_SERIES.items():
    INDICATOR_MAP[indicator_code] = {
        "indicator_name_zh": meta["indicator_name_zh"],
        "indicator_name_en": meta["indicator_name_en"],
        "unit": meta["unit"],
        "frequency": meta["frequency"],
        "seasonal_adjustment": meta["seasonal_adjustment"],
        "calculation": meta["calculation"],
        "sources": [
            {
                "organization": "National Bureau of Statistics of China",
                "dataset": meta["source_dataset"],
                "source_series_code": meta["source_series_code"],
            }
        ],
    }
