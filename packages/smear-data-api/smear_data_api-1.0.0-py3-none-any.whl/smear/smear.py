import json
import numpy as np
import pandas as pd
import urllib.request
from collections.abc import Iterable
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pandas")

"""
This module provides functions to interact with the Smart SMEAR API.
It allows users to fetch time series data, list available variables, and get metadata for specific variables.
The API provides data from the SMEAR (Station for Measuring Ecosystem-Atmosphere Relations) network, which is a research initiative in Finland.
The functions in this module include:

- getData: Fetch time series data for specified variables and dates.
- listAllData: List all available variables in the SMEAR database.
- getVariableMetadata: Get metadata for specific variables.

The module also includes helper functions to check the type of input data, construct URLs for API requests, and process the fetched data into a structured format.
"""

# Helper Functions
def isStr(obj):
    return isinstance(obj, str)


def isStrIterable(obj):
    return isinstance(obj, Iterable) and not isinstance(obj, str) and all(isinstance(elem, str) for elem in obj)


def isDatetime(obj):
    return isinstance(obj, datetime)


def isDatetimeIterable(obj):
    return isinstance(obj, Iterable) and all(isinstance(elem, datetime) for elem in obj)


def isNumeric(obj):
    try:
        float(obj)
        return True
    except ValueError:
        return False


def isNumericIterable(obj):
    return isinstance(obj, Iterable) and all(isNumeric(elem) for elem in obj)


def fetch_data_from_url(url):
    """Fetch data from a given URL and return a pandas DataFrame."""
    try:
        return pd.read_csv(url)
    except Exception as e:
        print(f"Error fetching data from URL: {e}")
        return pd.DataFrame([])


def process_data(data, col_names):
    """Process the raw data into a structured DataFrame."""
    if data.empty:
        return pd.DataFrame([])

    combined_datetime = pd.to_datetime(data[["Year", "Month", "Day", "Hour", "Minute", "Second"]])
    data.set_index(combined_datetime, inplace=True)
    data.drop(columns=["Year", "Month", "Day", "Hour", "Minute", "Second"], inplace=True)
    data.index.names = ['time']
    data = data.reindex(col_names, axis=1)
    data.columns = col_names
    return data


def construct_url(base_url, params):
    """Construct a URL with given base URL and parameters."""
    return base_url + "&".join([f"{key}={value}" for key, value in params.items()])


# Main Functions
def getData(variables, dates=None, start=None, end=None, quality='ANY', averaging='1', avg_type='NONE'):
    """Get timeseries of variables using Smart SMEAR API."""
    if isStrIterable(variables):
        col_names = list(variables)
        variable_string = ''.join([f'&tablevariable={x}' for x in variables])
    elif isStr(variables):
        col_names = [variables]
        variable_string = f'&tablevariable={variables}'
    else:
        raise ValueError('"variables" must be string or array of strings')

    if (start and end and dates) or not (start or end or dates):
        raise ValueError('Provide either "start" and "end" or "dates"')

    base_url = 'https://smear-backend-avaa-smear-prod.2.rahtiapp.fi/search/timeseries/csv?'

    if start and end:
        if isStr(start) and isStr(end):
            start, end = pd.to_datetime(start), pd.to_datetime(end)
        elif not (isDatetime(start) and isDatetime(end)):
            raise ValueError('"start" and "end" must be datetime objects or strings')

        params = {
            "from": start.strftime("%Y-%m-%dT%H:%M:%S").replace(':', '%3A'),
            "to": end.strftime("%Y-%m-%dT%H:%M:%S").replace(':', '%3A'),
            "quality": quality,
            "interval": averaging,
            "aggregation": avg_type,
        }
        url = construct_url(base_url, params)
        data = fetch_data_from_url(url)
        return process_data(data, col_names)

    elif dates:
        if isDatetimeIterable(dates):
            pass
        elif isDatetime(dates):
            dates = [dates]
        elif isStrIterable(dates):
            dates = pd.to_datetime(dates)
        elif isStr(dates):
            dates = [pd.to_datetime(dates)]
        else:
            raise ValueError('"dates" must be datetime object or string or array of datetime objects or strings')

        datas = []
        for t in dates:
            params = {
                "from": t.strftime("%Y-%m-%dT%H:%M:%S").replace(':', '%3A'),
                "to": (t + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S").replace(':', '%3A'),
                "quality": quality,
                "interval": averaging,
                "aggregation": avg_type,
            }
            url = construct_url(base_url, params)
            data = fetch_data_from_url(url)
            datas.append(process_data(data, col_names))

        return datas if len(datas) > 1 else datas[0]


def listAllData(search_term=None, verbose=False):
    """List and describe variables in the SMEAR database."""
    if search_term and not isStr(search_term):
        raise ValueError('"search_term" should be a string')

    if not isinstance(verbose, bool):
        raise ValueError('"verbose" should be True or False')

    variable_meta_url = "https://smear-backend-avaa-smear-prod.2.rahtiapp.fi/search/variable"
    nums = list("0123456789x")
    numssub = list("₀₁₂₃₄₅₆₇₈₉ₓ")

    with urllib.request.urlopen(variable_meta_url) as url:
        variablemetadata = json.loads(url.read().decode())

    df = pd.DataFrame(variablemetadata)
    df['title'] = df['title'].apply(lambda x: ''.join(nums[numssub.index(c)] if c in numssub else c for c in x))
    if search_term:
        df = df[df['title'].str.contains(search_term, case=False, na=False)]

    return df[['title', 'tableName', 'description', 'source']] if verbose else df[['title', 'tableName']]


def getVariableMetadata(variables):
    """Get variable metadata using Smart SMEAR API."""
    if isStrIterable(variables):
        variable_string = ''.join([f'&tablevariable={x}' for x in variables])
    elif isStr(variables):
        variable_string = f'&tablevariable={variables}'
    else:
        raise ValueError('"variables" must be string or array of strings')

    meta_url = f'https://smear-backend-avaa-smear-prod.2.rahtiapp.fi/search/variable?{variable_string}'
    try:
        with urllib.request.urlopen(meta_url) as url:
            return json.loads(url.read().decode())
    except Exception as e:
        print(f"Error fetching metadata: {e}")
        return []
