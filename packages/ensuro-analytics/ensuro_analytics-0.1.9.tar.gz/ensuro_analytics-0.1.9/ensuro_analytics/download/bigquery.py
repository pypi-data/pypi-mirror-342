"""Utilities for downloading and processing Ensuro data from BigQuery.

This module provides functionality to interact with Google BigQuery to fetch and process
Ensuro data, including:
- Policy data retrieval and processing
- Time series data management
- eToken metrics calculation
- Data type conversion and normalization
"""

import json

import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

from ensuro_analytics.download.api import OffchainAPI
from ensuro_analytics.download.base import ENSURO_API_URL
from ensuro_analytics.download.utils import etoken_blockshot_processing as etk_processing

DEFAULT_POLICIES_TABLE_COLUMNS = [
    "id",
    "ensuro_id",
    "payout",
    "loss_prob",
    "jr_scr",
    "sr_scr",
    "pure_premium",
    "ensuro_commission",
    "partner_commission",
    "jr_coc",
    "sr_coc",
    "start",
    "expiration",
    "actual_payout",
    "expired_on",
    "premium",
    "active",
    "progress",
    "duration_expected",
    "duration_actual",
    "risk_module",
    "risk_module_name",
    "quote",
    "events",
    "replaces",
    "replaced_by",
    "splitter1",
    "splitter2",
    "date_price_applied",
]

DATETIME_COLUMNS = ["date", "start", "expiration", "expired_on", "date_price_applied"]
NUMERICAL_COLUMNS = [
    "payout",
    "loss_prob",
    "jr_scr",
    "sr_scr",
    "pure_premium",
    "ensuro_commission",
    "partner_commission",
    "jr_coc",
    "sr_coc",
    "actual_payout",
    "premium",
    "progress",
    "duration_expected",
    "duration_actual",
]


class BigQueryInterface:
    """Interface for interacting with Google BigQuery API.

    This class provides methods to fetch and process data from BigQuery tables,
    including policy data, time series, and eToken metrics.

    Attributes:
        project_id: The Google Cloud project ID.
        dataset_name: The name of the dataset in BigQuery.
        account_key_path: Optional path to the service account key file.
        policies_table_columns: List of columns to fetch from the policies table.
        credentials: Google Auth credentials for BigQuery client.
        Client: BigQuery client instance.

    Methods:
        _date_cols_to_datetime: Convert specified columns to datetime format.
        _bytes_to_dict: Convert bytes columns to dictionaries.
        sql: Execute SQL queries and return results as DataFrame.
        policies_table: Fetch and process policy data.
        time_series_table: Fetch time series data.
        etoken_blockshot: Fetch eToken blockshot data.
        token_metrics: Calculate eToken metrics with optional insurance returns.
        fetch_data: Fetch data from specified tables.
    """

    def __init__(
        self,
        project_id: str,
        dataset_name: str,
        account_key_path: str | None = None,
        policies_table_columns: list[str] | None = None,
    ):
        """Initialize the BigQuery interface.

        Args:
            project_id: The Google Cloud project ID.
            dataset_name: The name of the dataset in BigQuery.
            account_key_path: Optional path to the service account key file.
            policies_table_columns: Optional list of columns to fetch from policies table.
        """
        self.project_id = project_id
        self.dataset_name = dataset_name
        self.account_key_path = account_key_path
        self.credentials = None

        if self.account_key_path is not None:
            self.credentials = service_account.Credentials.from_service_account_file(self.account_key_path)

        self.Client = bigquery.Client(credentials=self.credentials, project=self.project_id)

        if policies_table_columns is None:
            self.policies_table_columns = DEFAULT_POLICIES_TABLE_COLUMNS
        else:
            self.policies_table_columns = policies_table_columns

    @staticmethod
    def _date_cols_to_datetime(df: pd.DataFrame, columns: list[str] = DATETIME_COLUMNS):
        """
        Converts the specified columns of the dataframe to datetime.

        Args:
            df: DataFrame containing the columns to convert.
            columns: List of column names to convert. Defaults to DATETIME_COLUMNS.

        Returns:
            DataFrame with specified columns converted to datetime format.
        """
        for col in columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col]).dt.tz_localize(None)
        return df

    @staticmethod
    def _bytes_to_dict(col: pd.Series) -> pd.Series:
        """Convert bytes columns to dictionaries.

        Args:
            col: Series containing bytes or JSON strings to convert.

        Returns:
            Series with bytes/JSON strings converted to dictionaries.
        """
        quote_types = col.apply(type).unique()
        if bytes in quote_types:
            col = col.apply(lambda x: x.decode("utf-8") if isinstance(x, bytes) else x)
            col = col.apply(lambda x: json.loads(x) if isinstance(x, str) else x)
        return col

    def sql(self, sql_query: str) -> pd.DataFrame:
        """Execute a SQL query and return results as DataFrame.

        Args:
            sql_query: The SQL query to execute.

        Returns:
            DataFrame containing the query results.
        """
        df = self.Client.query(sql_query).to_dataframe()
        return df

    def policies_table(self, limit: int | None = None) -> pd.DataFrame:
        """
        Fetches data from the policies table and returns it as a dataframe.

        Args:
            limit: Optional maximum number of rows to return.

        Returns:
            DataFrame containing processed policy data.
        """
        columns_str = ", ".join(self.policies_table_columns)
        sql_query = f"SELECT * FROM `{self.project_id}.{self.dataset_name}.policies_quant`"
        if limit is not None:
            sql_query += f" ORDER BY id DESC LIMIT {limit}"
        sql_query = f"SELECT {columns_str} FROM ({sql_query}) ORDER BY id ASC"

        data = self._date_cols_to_datetime(self.sql(sql_query))
        data = self.format_columns_dtypes(data)
        data["quote"] = self._bytes_to_dict(data.quote)

        return data

    @staticmethod
    def format_columns_dtypes(data: pd.DataFrame) -> pd.DataFrame:
        """
        Format columns in the DataFrame to appropriate data types.
        """
        for col in NUMERICAL_COLUMNS:
            data[col] = data[col].astype(float)
        data["active"] = data["active"].astype(bool)
        return data

    def time_series_table(self) -> pd.DataFrame:
        """Fetch time series data from BigQuery.

        Returns:
            DataFrame containing processed time series data.
        """
        sql_query = f"SELECT * FROM `{self.project_id}.{self.dataset_name}.time_series`"
        return self._date_cols_to_datetime(self.sql(sql_query))

    def etoken_blockshot(self) -> pd.DataFrame:
        """Fetch eToken blockshot data from BigQuery.

        Returns:
            DataFrame containing processed eToken blockshot data.
        """
        sql_query = f"SELECT * FROM `{self.project_id}.{self.dataset_name}.etoken_block_shot`"
        return self._date_cols_to_datetime(self.sql(sql_query))

    def token_metrics(self, include_insurance_returns: bool = False) -> pd.DataFrame:
        """Calculate eToken metrics with optional insurance returns.

        This function combines eToken blockshot data with LP events and API data
        to calculate comprehensive token metrics.

        Args:
            include_insurance_returns: If True, includes returns from Ensuro's
                insurance activity. If False, only includes compound returns from
                insurance activity and investments.

        Returns:
            DataFrame containing processed token metrics.
        """
        etoken_blockshot = self.etoken_blockshot()

        offchain_api = OffchainAPI(ENSURO_API_URL)

        lps = pd.json_normalize(offchain_api.multi_page_get("lpevents"), sep="_")
        etokens_api_query = offchain_api.get("etokens").json()

        token_metrics = etk_processing.blocks_shots_to_token_metrics(
            etoken_blockshot, lps, etokens_api_query
        )

        if include_insurance_returns is True:
            riskmodules, sr_etks_to_rm, jr_etks_to_rm = etk_processing.get_etokens_to_risk_modules_map(
                offchain_api
            )
            policies = self.policies_table()
            insurance_returns = etk_processing.build_insurance_returns(
                token_metrics, policies, sr_etks_to_rm, jr_etks_to_rm
            )
            token_metrics["dividend_insurance"] = insurance_returns.dividend_insurance

        return token_metrics

    def fetch_data(self, table: str) -> pd.DataFrame:
        """Fetch data from specified tables.

        Args:
            table: Name of the table to fetch data from. Must be either 'portfolio'
                or 'time-series'.

        Returns:
            DataFrame containing the fetched data.

        Raises:
            AssertionError: If the table name is not 'portfolio' or 'time-series'.
        """
        assert table in [
            "portfolio",
            "time-series",
        ], "table must be either 'portfolio' or 'time-series'"

        if table == "portfolio":
            data = self.policies_table()
        elif table == "time-series":
            data = self.time_series_table()

        return data
