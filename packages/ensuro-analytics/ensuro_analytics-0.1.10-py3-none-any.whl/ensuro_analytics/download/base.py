"""
This module contains the functions to download data from Ensuro's API and BigQuery.
"""

ENSURO_API_URL = "https://offchain-v2.ensuro.co/api/"


def get_from_quote(x, field):
    """
    This function attempts to retrieve a specific field from policies' metadata in the 'quote' column.

    Parameters:
    x (dict): The quote from which to retrieve the field. It is expected to be a dictionary with a "data" key.
    field (str): The name of the field to retrieve from the quote.

    Returns:
    The value of the specified field if it exists, None otherwise.
    """
    if not isinstance(x, dict):
        return None
    try:
        return x["data"][field]
    except (KeyError, TypeError):
        return None
