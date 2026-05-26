import argparse
import json
from storage.database import query_observations

def to_json(country, indicator, start=None, end=None, frequency=None):
    df = query_observations(country, indicator, start, end, frequency)
    request_obj = {"country": country, "indicator_code": indicator, "start_date": start, "end_date": end, "frequency": frequency}
    if df.empty:
        return {"request": request_obj, "series": None, "error": {"message": "No data found"}}
    first = df.iloc[0].to_dict()
    observations = []
    for _, row in df.iterrows():
        val = row.get("value")
        observations.append({"date": str(row.get("date")), "value": None if val != val else float(val), "status": row.get("status") or "final"})
    return {
        "request": request_obj,
        "series": {
            "series_id": first.get("series_id"),
            "indicator_name_zh": first.get("indicator_name_zh"),
            "indicator_name_en": first.get("indicator_name_en"),
            "country_name_zh": first.get("country_name_zh"),
            "country_name_en": first.get("country_name_en"),
            "country_code": first.get("country_code"),
            "frequency": first.get("frequency"),
            "unit": first.get("unit"),
            "seasonal_adjustment": first.get("seasonal_adjustment"),
            "calculation": first.get("calculation"),
            "source": {"organization": first.get("source_organization"), "dataset": first.get("source_dataset"), "source_series_code": first.get("source_indicator_code"), "source_url": first.get("source_url")},
            "last_updated": first.get("last_updated"),
            "observations": observations,
        },
        "error": None
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--country", required=True)
    parser.add_argument("--indicator", required=True)
    parser.add_argument("--start", default=None)
    parser.add_argument("--end", default=None)
    parser.add_argument("--frequency", default=None)
    args = parser.parse_args()
    print(json.dumps(to_json(args.country, args.indicator, args.start, args.end, args.frequency), ensure_ascii=False, indent=2))
