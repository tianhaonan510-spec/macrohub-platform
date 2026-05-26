import time
import logging
from datetime import datetime
from typing import Dict, List, Any

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config import COUNTRIES, INDICATOR_MAP, START_YEAR, END_YEAR, DATA_RAW, LOG_DIR

DATA_RAW.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "collect.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
)

def _session() -> requests.Session:
    s = requests.Session()
    retry = Retry(total=3, backoff_factor=0.8, status_forcelist=[429, 500, 502, 503, 504])
    s.mount("https://", HTTPAdapter(max_retries=retry))
    s.mount("http://", HTTPAdapter(max_retries=retry))
    return s

def _fetch_one(country_iso2: str, source_series_code: str, start_year: int, end_year: int) -> List[Dict[str, Any]]:
    url = (
        f"https://api.worldbank.org/v2/country/{country_iso2}/indicator/{source_series_code}"
        f"?format=json&per_page=20000&date={start_year}:{end_year}"
    )
    resp = _session().get(url, timeout=30)
    resp.raise_for_status()
    payload = resp.json()
    if not isinstance(payload, list) or len(payload) < 2 or payload[1] is None:
        return []
    rows = []
    for item in payload[1]:
        rows.append({
            "country_code": country_iso2,
            "country_name": item.get("country", {}).get("value"),
            "source_indicator_code": source_series_code,
            "source_indicator_name": item.get("indicator", {}).get("value"),
            "date": item.get("date"),
            "value": item.get("value"),
            "source_organization": "World Bank",
            "source_dataset": "World Development Indicators",
            "source_url": url,
            "retrieved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
            "status": "final",
        })
    return rows

def collect_worldbank() -> pd.DataFrame:
    all_rows = []
    source_codes = sorted({
        src["source_series_code"]
        for meta in INDICATOR_MAP.values()
        for src in meta["sources"]
        if src["organization"] == "World Bank"
    })
    total = len(COUNTRIES) * len(source_codes)
    done = 0
    for country_iso2 in COUNTRIES:
        for source_code in source_codes:
            done += 1
            try:
                rows = _fetch_one(country_iso2, source_code, START_YEAR, END_YEAR)
                all_rows.extend(rows)
                logging.info(f"World Bank OK {done}/{total}: {country_iso2} {source_code}, rows={len(rows)}")
                print(f"[WorldBank] {done}/{total} {country_iso2} {source_code}: {len(rows)} rows")
                time.sleep(0.15)
            except Exception as e:
                logging.exception(f"World Bank FAILED: {country_iso2} {source_code}: {e}")
                print(f"[WorldBank] FAILED {country_iso2} {source_code}: {e}")
    df = pd.DataFrame(all_rows)
    out = DATA_RAW / "worldbank_raw.csv"
    df.to_csv(out, index=False, encoding="utf-8-sig")
    print(f"[WorldBank] saved: {out}, shape={df.shape}")
    return df

if __name__ == "__main__":
    collect_worldbank()
