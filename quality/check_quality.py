import pandas as pd
from config import DATA_CLEAN

def run_quality_checks() -> pd.DataFrame:
    path = DATA_CLEAN / "macro_observations.csv"
    if not path.exists():
        raise FileNotFoundError(f"未找到标准化数据：{path}")
    df = pd.read_csv(path)
    key_cols = ["country_code", "indicator_code", "date", "source_organization", "source_dataset"]
    checks = [
        {"check_item": "row_count", "value": len(df), "status": "info"},
        {"check_item": "missing_value_count", "value": int(df["value"].isna().sum()), "status": "warning" if df["value"].isna().any() else "ok"},
        {"check_item": "duplicate_key_count", "value": int(df.duplicated(key_cols).sum()), "status": "warning" if df.duplicated(key_cols).any() else "ok"},
        {"check_item": "missing_source_url_count", "value": int(df["source_url"].isna().sum()), "status": "warning" if df["source_url"].isna().any() else "ok"},
        {"check_item": "country_count", "value": int(df["country_code"].nunique()), "status": "info"},
        {"check_item": "indicator_count", "value": int(df["indicator_code"].nunique()), "status": "info"},
    ]
    report = pd.DataFrame(checks)
    out = DATA_CLEAN / "quality_report.csv"
    report.to_csv(out, index=False, encoding="utf-8-sig")
    print(f"[Quality] saved: {out}")
    return report

if __name__ == "__main__":
    run_quality_checks()
