# import argparse
# from collectors.worldbank_collector import collect_worldbank
# from standardizer.standardize import standardize_worldbank, build_indicator_master, build_source_mapping, build_country_master
# from quality.check_quality import run_quality_checks
# from storage.database import init_db
#
# def run_all():
#     print("Step 1/5: 构建元数据字典")
#     build_indicator_master(); build_source_mapping(); build_country_master()
#     print("Step 2/5: 采集 World Bank 数据")
#     collect_worldbank()
#     print("Step 3/5: 标准化处理")
#     standardize_worldbank()
#     print("Step 4/5: 数据质量检查")
#     run_quality_checks()
#     print("Step 5/5: SQLite 入库")
#     init_db()
#     print("全部完成。下一步运行：uvicorn api_service.app:app --reload")
#
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--collect-only", action="store_true", help="只采集 World Bank 原始数据")
#     parser.add_argument("--standardize-only", action="store_true", help="只做标准化")
#     parser.add_argument("--quality-only", action="store_true", help="只做质量检查")
#     parser.add_argument("--db-only", action="store_true", help="只入库")
#     args = parser.parse_args()
#     if args.collect_only:
#         collect_worldbank()
#     elif args.standardize_only:
#         standardize_worldbank()
#     elif args.quality_only:
#         run_quality_checks()
#     elif args.db_only:
#         init_db()
#     else:
#         run_all()






# -*- coding: utf-8 -*-
"""
MacroHub 数据采集与入库主程序
"""

import argparse
import pandas as pd

from config import DATA_RAW, DATA_CLEAN
from collectors.worldbank_collector import collect_worldbank
from standardizer.standardize import standardize_worldbank
from quality.check_quality import run_quality_checks
from storage.database import init_db


def merge_imf_data():
    main_file = DATA_CLEAN / "macro_observations.csv"
    imf_file = DATA_RAW / "imf" / "imf_standardized.csv"

    if not main_file.exists():
        raise FileNotFoundError(f"未找到主数据文件：{main_file}")

    df_main = pd.read_csv(main_file, encoding="utf-8-sig")

    if not imf_file.exists():
        print("[Merge] 未发现 IMF 标准化文件，跳过 IMF 合并。")
        return df_main

    df_imf = pd.read_csv(imf_file, encoding="utf-8-sig")

    print(f"[Merge] 主表 rows={len(df_main)}")
    print(f"[Merge] IMF rows={len(df_imf)}")

    for col in df_main.columns:
        if col not in df_imf.columns:
            df_imf[col] = None

    df_imf = df_imf[df_main.columns]

    df_all = pd.concat([df_main, df_imf], ignore_index=True)

    df_all = df_all.drop_duplicates(
        subset=[
            "country_code",
            "indicator_code",
            "date",
            "source_organization",
            "source_dataset"
        ],
        keep="last"
    )

    df_all = df_all.sort_values([
        "source_organization",
        "country_code",
        "indicator_code",
        "date"
    ])

    df_all.to_csv(main_file, index=False, encoding="utf-8-sig")

    print(f"[Merge] 合并后 rows={len(df_all)}")
    print(f"[Merge] saved: {main_file}")

    return df_all


def run_full_pipeline():
    print("Step 1/5: World Bank 数据采集")
    collect_worldbank()

    print("Step 2/5: World Bank 标准化")
    standardize_worldbank()

    print("Step 3/5: 合并 IMF 数据")
    merge_imf_data()

    print("Step 4/5: 数据质量检查")
    run_quality_checks()

    print("Step 5/5: SQLite 入库")
    init_db()

    print("全部完成。")


def run_merge_imf_only():
    print("Step 1/3: 合并 IMF 数据")
    merge_imf_data()

    print("Step 2/3: 数据质量检查")
    run_quality_checks()

    print("Step 3/3: SQLite 入库")
    init_db()

    print("IMF 合并与入库完成。请刷新 Streamlit 页面查看。")


def main():
    parser = argparse.ArgumentParser(
        description="MacroHub 数据采集、标准化、合并与入库主程序"
    )

    parser.add_argument("--collect-only", action="store_true")
    parser.add_argument("--standardize-only", action="store_true")
    parser.add_argument("--merge-imf-only", action="store_true")

    args = parser.parse_args()

    if args.collect_only:
        collect_worldbank()
        return

    if args.standardize_only:
        standardize_worldbank()
        return

    if args.merge_imf_only:
        run_merge_imf_only()
        return

    run_full_pipeline()


if __name__ == "__main__":
    main()