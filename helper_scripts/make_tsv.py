from helper_scripts.dbcon.queries import (
    query_store_apps_companies,
    query_store_apps,
    query_live_store_apps,
    query_store_apps_metrics,
)

import pandas as pd
import numpy as np

from helper_scripts.config import get_logger

logger = get_logger(__name__)

TABLES_DICT = {
    # "store_apps_companies": query_store_apps_companies, # still too big
    # "store_apps": query_store_apps,
    "store_apps_metrics": query_store_apps_metrics,
    "live_store_apps": query_live_store_apps,
}


def make_tsv(file_name: str):
    logger.info(f"{file_name} start")
    df = TABLES_DICT[file_name]()
    if "store_last_updated" in df.columns:
        df["store_last_updated"] = pd.to_datetime(df["store_last_updated"]).dt.strftime(
            "%Y-%m-%d"
        )
    if "appgoblin_updated_at" in df.columns:
        df["appgoblin_updated_at"] = pd.to_datetime(
            df["appgoblin_updated_at"]
        ).dt.strftime("%Y-%m-%d")
    if "developer_id" in df.columns:
        df["developer_id"] = np.where(
            (df["store"] == "Apple") & (df["developer_id"].str.contains("\\.0")),
            df["developer_id"].str.replace("\\.0", ""),
            df["developer_id"],
        )
    logger.info(f"{file_name} write {df.shape[0]} rows")
    df.to_csv("data/" + file_name + ".tsv.xz", sep="\t", index=False, compression="xz")
    logger.info(f"{file_name} done")


if __name__ == "__main__":
    logger.info("start")
    for file_name in TABLES_DICT.keys():
        make_tsv(file_name)
