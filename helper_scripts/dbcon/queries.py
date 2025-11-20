"""Query database for backend API."""

import pathlib
from typing import Iterator, Union
import numpy as np

import pandas as pd
from sqlalchemy import text

from helper_scripts.config import MODULE_DIR, get_logger
from helper_scripts.dbcon.connections import get_db_connection

logger = get_logger(__name__)


SQL_DIR = pathlib.Path(MODULE_DIR, "dbcon/sql/")


def load_sql_file(file_name: str) -> str:
    """Load local SQL file based on file name."""
    file_path = pathlib.Path(SQL_DIR, file_name)
    with file_path.open() as file:
        return text(file.read())


QUERY_STORE_APPS = load_sql_file(
    "query_store_apps.sql",
)
QUERY_STORE_APPS_METRICS = load_sql_file(
    "query_store_apps_metrics.sql",
)
QUERY_APPS_COMPANIES = load_sql_file(
    "query_store_apps_companies.sql",
)
QUERY_LIVE_STORE_APPS = load_sql_file(
    "query_live_store_apps.sql",
)
QUERY_COMPANY_ADSTXT_PUBLISHER_ID = load_sql_file(
    "query_company_adstxt_publisher_id.sql"
)
QUERY_AD_DOMAINS = load_sql_file("query_ad_domains.sql")


def query_store_apps() -> pd.DataFrame:
    """Get all apps and developer info."""
    df = pd.read_sql(QUERY_STORE_APPS, con=DBCON.engine)
    return df


def query_store_apps_metrics() -> pd.DataFrame:
    """Get all apps and developer info."""
    df = pd.read_sql(QUERY_STORE_APPS_METRICS, con=DBCON.engine)
    return df


def query_store_apps_companies() -> pd.DataFrame:
    """Get all apps and developer info."""
    df = pd.read_sql(QUERY_APPS_COMPANIES, con=DBCON.engine)
    return df


def query_live_store_apps() -> pd.DataFrame:
    """Get all apps and developer info."""
    df = pd.read_sql(QUERY_LIVE_STORE_APPS, con=DBCON.engine)
    return df


def query_ad_domains() -> pd.DataFrame:
    """Get all ad domains"""
    df = pd.read_sql(QUERY_AD_DOMAINS, con=DBCON.engine)
    return df


def get_company_adstxt_publisher_id_apps_raw(
    ad_domain_url: str, chunksize: Union[int, None] = None
) -> Union[pd.DataFrame, Iterator[pd.DataFrame]]:
    """
    Get ad domain publisher id with optional chunked processing.

    Args:
        ad_domain_url: Domain URL to query
        chunksize: If provided, returns an iterator of DataFrames with specified chunk size
                  If None, returns a single DataFrame
    """
    # Convert the SQL query to use parameters safely

    # Read from database in chunks if chunksize is specified
    df_iterator = pd.read_sql(
        QUERY_COMPANY_ADSTXT_PUBLISHER_ID,
        DBCON.engine,
        params={"ad_domain_url": ad_domain_url},
        chunksize=chunksize,
    )

    if chunksize is None:
        # If no chunking, process the entire DataFrame at once
        df = next(df_iterator)
        return process_dataframe(df)
    else:
        # If chunking, return a generator that processes each chunk
        return (process_dataframe(chunk) for chunk in df_iterator)


def process_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process a DataFrame chunk with the required transformations.
    """
    # Create a copy to avoid modifying the original DataFrame
    df = df.copy()

    # Apply transformations
    df["store"] = df["store"].replace({1: "Android", 2: "iOS"})
    df["developer_id"] = df["developer_id"].astype(str)

    # Use numpy.select for more efficient conditional logic
    conditions = [df["store"] == "Android"]
    choices = ["https://play.google.com/store/apps/details?id=" + df["store_id"]]
    default = "https://apps.apple.com/-/app/-/id" + df["store_id"]

    df["store_url"] = np.select(conditions, choices, default=default)

    return df


logger.info("set db engine")
DBCON = get_db_connection(use_ssh_tunnel=False)
DBCON.set_engine()
