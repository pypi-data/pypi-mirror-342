"""
Functions.

Tree of TransformRows functions.

"""
from typing import List, Optional
import requests
import numpy as np
from numba import njit
from datetime import datetime
import pytz
from zoneinfo import ZoneInfo
from dateutil import parser
import pandas
from ...conf import BARCODELOOKUP_API_KEY
from ...utils.executor import getFunction


def apply_function(
    df: pandas.DataFrame,
    field: str,
    fname: str,
    column: Optional[str] = None,
    **kwargs
) -> pandas.DataFrame:
    """
    Apply any scalar function to a column in the DataFrame.

    Parameters:
    - df: pandas DataFrame
    - field: The column where the result will be stored.
    - fname: The name of the function to apply.
    - column: The column to which the function is applied (if None, apply to `field` column).
    - **kwargs: Additional arguments to pass to the function.
    """

    # Retrieve the scalar function using getFunc
    try:
        func = getFunction(fname)
    except Exception:
        raise

    # If a different column is specified, apply the function to it,
    # but save result in `field`
    try:
        if column is not None:
            df[field] = df[column].apply(lambda x: func(x, **kwargs))
        else:
            if field not in df.columns:
                # column doesn't exist
                df[field] = None
            # Apply the function to the field itself
            df[field] = df[field].apply(lambda x: func(x, **kwargs))
    except Exception as err:
        print(
            f"Error in apply_function for field {field}:", err
        )
    return df


def get_product(row, field, columns):
    """
    Retrieves product information from the Barcode Lookup API based on a barcode.

    :param row: The DataFrame row containing the barcode.
    :param field: The name of the field containing the barcode.
    :param columns: The list of columns to extract from the API response.
    :return: The DataFrame row with the product information.
    """

    barcode = row[field]
    url = f'https://api.barcodelookup.com/v3/products?barcode={barcode}&key={BARCODELOOKUP_API_KEY}'
    response = requests.get(url)
    result = response.json()['products'][0]
    for col in columns:
        try:
            row[col] = result[col]
        except KeyError:
            row[col] = None
    return row


def upc_to_product(
    df: pandas.DataFrame,
    field: str,
    columns: list = ['barcode_formats', 'mpn', 'asin', 'title', 'category', 'model', 'brand']
) -> pandas.DataFrame:
    """
    Converts UPC codes in a DataFrame to product information using the Barcode Lookup API.

    :param df: The DataFrame containing the UPC codes.
    :param field: The name of the field containing the UPC codes.
    :param columns: The list of columns to extract from the API response.
    :return: The DataFrame with the product information.
    """
    try:
        df = df.apply(lambda x: get_product(x, field, columns), axis=1)
        return df
    except Exception as err:
        print(f"Error on upc_to_product {field}:", err)
        return df

def day_of_week(
    df: pandas.DataFrame,
    field: str,
    column: str,
    locale: str = 'en_US.utf8'
) -> pandas.DataFrame:
    """
    Extracts the day of the week from a date column.

    :param df: The DataFrame containing the date column.
    :param field: The name of the field to store the day of the week.
    :param column: The name of the date column.
    :return: The DataFrame with the day of the week.
    """
    try:
        df[field] = df[column].dt.day_name(locale=locale)
        return df
    except Exception as err:
        print(f"Error on day_of_week {field}:", err)
        return df

def duration(
    df: pandas.DataFrame,
    field: str,
    columns: List[str],
    unit: str = 's'
) -> pandas.DataFrame:
    """
    Converts a duration column to a specified unit.

    :param df: The DataFrame containing the duration column.
    :param field: The name of the field to store the converted duration.
    :param column: The name of the duration column.
    :param unit: The unit to convert the duration to.
    :return: The DataFrame with the converted duration.
    """
    try:
        if unit == 's':
            _unit = 1.0
        if unit == 'm':
            _unit = 60.0
        elif unit == 'h':
            _unit = 3600.0
        elif unit == 'd':
            _unit = 86400.0
        # Calculate duration in minutes as float
        df[field] = (
            (df[columns[1]] - df[columns[0]]).dt.total_seconds() / _unit
        )
        return df
    except Exception as err:
        print(f"Error on duration {field}:", err)
        return df


def get_moment(
    df: pandas.DataFrame,
    field: str,
    column: str,
    moments: List[tuple] = None,
) -> pandas.DataFrame:
    """
    df: pandas DataFrame
    column: name of the column to compare (e.g. "updated_hour")
    ranges: list of tuples [(label, (start, end)), ...]
            e.g. [("night",(0,7)), ("morning",(7,10)), ...]
    returns: a Series of labels corresponding to each row
    """
    if not moments:
        moments = [
            ("night", (0, 7)),   # >= 0 and < 7
            ("morning", (7, 10)),  # >= 7 and < 10
            ("afternoon", (10, 16)),  # >= 10 and < 16
            ("evening", (16, 20)),  # >= 16 and < 20
            ("night", (20, 24)),  # >= 20 and < 24 (or use float("inf") for open-ended)
        ]
    conditions = [
        (df[column] >= start) & (df[column] < end)
        for _, (start, end) in moments
    ]
    df[field] = np.select(conditions, [label for label, _ in moments], default=None)
    return df


def fully_geoloc(
    df: pandas.DataFrame,
    field: str,
    columns: List[tuple],
    inverse: bool = False
) -> pandas.DataFrame:
    """
    Adds a boolean column (named `field`) to `df` that is True when,
    for each tuple in `columns`, all the involved columns are neither NaN nor empty.

    Parameters:
        df (pd.DataFrame): The DataFrame.
        field (str): The name of the output column.
        columns (list of tuple of str): List of tuples, where each tuple
            contains column names that must be valid (non-null and non-empty).
            Example: [("start_lat", "start_long"), ("end_lat", "end_log")]

    Returns:
        pd.DataFrame: The original DataFrame with the new `field` column.
    """
    # Start with an initial mask that's True for all rows.
    mask = pandas.Series(True, index=df.index)

    # Loop over each tuple of columns, then each column in the tuple.
    for col_group in columns:
        for col in col_group:
            if inverse:
                mask &= df[col].isna() | (df[col] == "")
            else:
                mask &= df[col].notna() & (df[col] != "")

    df[field] = mask
    return df


def any_tuple_valid(
    df: pandas.DataFrame,
    field: str,
    columns: List[tuple]
) -> pandas.DataFrame:
    """
    Adds a boolean column (named `field`) to `df` that is True when
    any tuple in `columns` has all of its columns neither NaN nor empty.

    Parameters:
        df (pd.DataFrame): The DataFrame.
        field (str): The name of the output column.
        columns (list of tuple of str): List of tuples, where each tuple
            contains column names that must be checked.
            Example: [("start_lat", "start_long"), ("end_lat", "end_log")]

    Returns:
        pd.DataFrame: The original DataFrame with the new `field` column.
    """
    # Start with an initial mask that's False for all rows
    result = pandas.Series(False, index=df.index)

    # Loop over each tuple of columns
    for col_group in columns:
        # For each group, assume all columns are valid initially
        group_all_valid = pandas.Series(True, index=df.index)

        # Check that all columns in this group are non-null and non-empty
        for col in col_group:
            group_all_valid &= df[col].notna() & (df[col] != "")

        # If all columns in this group are valid, update the result
        result |= group_all_valid

    df[field] = result
    return df


@njit
def haversine_distance(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
    unit: str = 'km'
) -> float:
    """Distance between two points on Earth in kilometers."""
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = np.radians(lat1), np.radians(lon1), np.radians(lat2), np.radians(lon2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    # Select radius based on unit
    if unit == 'km':
        r = 6371.0  # Radius of earth in kilometers
    elif unit == 'm':
        r = 6371000.0  # Radius of earth in meters
    elif unit == 'mi':
        r = 3956.0  # Radius of earth in miles
    else:
        # Numba doesn't support raising exceptions, so default to km
        r = 6371.0

    return c * r

def calculate_distance(
    df: pandas.DataFrame,
    field: str,
    columns: List[tuple],
    unit: str = 'km',
    chunk_size: int = 1000
) -> pandas.DataFrame:
    """
    Add a distance column to a dataframe.

    Args:
        df: pandas DataFrame with columns 'latitude', 'longitude', 'store_lat', 'store_lng'
        columns: list of tuples with column names for coordinates
               - First tuple: [latitude1, longitude1]
               - Second tuple: [latitude2, longitude2]
        unit: unit of distance ('km' for kilometers, 'm' for meters, 'mi' for miles)
        chunk_size: number of rows to process at once for large datasets

    Returns:
        df with additional 'distance_km' column
    """
    result = df.copy()
    result[field] = np.nan
    # Unpack column names
    (lat1_col, lon1_col), (lat2_col, lon2_col) = columns
    try:
        for i in range(0, len(df), chunk_size):
            chunk = df.iloc[i:i + chunk_size]
            # Convert to standard NumPy arrays before passing to haversine_distance
            lat1_values = chunk[lat1_col].to_numpy(dtype=np.float64)
            lon1_values = chunk[lon1_col].to_numpy(dtype=np.float64)
            lat2_values = chunk[lat2_col].to_numpy(dtype=np.float64)
            lon2_values = chunk[lon2_col].to_numpy(dtype=np.float64)
            result.loc[chunk.index, field] = haversine_distance(
                lat1_values,
                lon1_values,
                lat2_values,
                lon2_values,
                unit=unit
            )
    except Exception as err:
        print(f"Error on calculate_distance {field}:", err)
    return result


def drop_timezone(
    df: pandas.DataFrame,
    field: str,
    column: Optional[str] = None
) -> pandas.DataFrame:
    """
    Drop the timezone information from a datetime column.

    Args:
        df: pandas DataFrame with a datetime column
        field: name of the datetime column

    Returns:
        df with timezone-free datetime column
    """
    try:
        if column is None:
            column = field

        series = df[column]
        if pandas.api.types.is_datetime64tz_dtype(series):
            # This is a regular tz-aware pandas Series
            df[field] = series.dt.tz_localize(None)
            return df

        elif series.dtype == 'object':
            # Object-dtype: apply tz-localize(None) to each element
            def remove_tz(x):
                if isinstance(x, (pandas.Timestamp, datetime)) and x.tzinfo is not None:
                    return x.replace(tzinfo=None)
                return x  # leave as-is (could be NaT, None, or already naive)

            df[field] = series.apply(remove_tz).astype('datetime64[ns]')
            return df

        else:
            # already naive or not datetime
            df[field] = series
            return df
    except Exception as err:
        print(f"Error on drop_timezone {field}:", err)
    return df


def convert_timezone(
    df: pandas.DataFrame,
    field: str,
    column: Optional[str] = None,
    from_tz: Optional[str] = 'UTC',
    tz_column: Optional[str] = None,
    default_timezone: str = 'America/Chicago',
) -> pandas.DataFrame:
    """
    Convert a datetime column to a specified timezone.

    Args:
        df: pandas DataFrame with a datetime column
        field: name of the datetime column
        column: name of the column to convert (if different from field)
        from_tz: fallback timezone to use for naive datetimes
        tz_column: name of the timezone column (for row-specific timezones)

    Returns:
        df with converted datetime column
    """
    try:
        if column is None:
            column = field
        # Create a new column to avoid touching the original.
        if field != column:
            df[field] = df[column].copy()

        # Handle timezone info
        # Ensure the column is datetime-like
        # df[field] = pandas.to_datetime(df[field], errors='coerce')
        # 1. For timestamps with timezone info, keep as is
        # 2. For naive timestamps, localize to from_tz
        if df[field].dt.tz is None:
            df[field] = df[field].dt.tz_localize(from_tz, ambiguous='infer', nonexistent='raise')

        infer_dst = np.array([False] * df.shape[0])
        df['timezone_obj'] = df[tz_column].apply(
            lambda tz: ZoneInfo(tz) if pandas.notnull(tz) else ZoneInfo(default_timezone)
        )

        def row_converter(i, row, infer_dst_flag: bool = None):
            dt = row[field]

            # if is none, convert to NaT
            if infer_dst_flag is None:
                infer_dst_flag = infer_dst[i]

            # Step 2: if timezone is UTC, no conversion needed
            if dt.tzinfo == pytz.utc:
                return dt

            if pandas.isna(dt):
                return dt

            # Step 1: if datetime is naive, localize it to UTC
            try:
                if dt.tzinfo is None:
                    dt = pandas.Timestamp(dt).tz_localize(
                        from_tz,  # fallback if tz ambiguous
                        ambiguous=True,
                        nonexistent='raise',
                    ).dt.tz_convert(from_tz)
                else:
                    dt = dt.astimezone(from_tz)  # normalize to UTC

                return dt.to_datetime64()
            except Exception as e:
                print(f"Error in UTC Transformation {dt}: {e}")
                return dt

        # Apply with row-wise context + external `infer_dst` flag
        if not tz_column:
            # Convert to UTC
            df[field] = [
                row_converter(i, row, infer_dst_flag=infer_dst[i])
                for i, row in df.iterrows()
            ]
        # If there's a row-specific timezone column, convert each row to its specific timezone
        if tz_column and tz_column in df.columns:
            def safe_converter(i, row):
                dt = row[field]
                tz = row['timezone_obj']
                try:
                    dt = dt.tz_convert('UTC')
                    dt = dt.tz_convert(tz)
                    return dt
                except Exception as e:
                    print(f"Error converting timezone for {dt}: {e}")
                    return dt
            # Apply the conversion row by row
            df[field] = [
                safe_converter(i, row)
                for i, row in df.iterrows()
            ]

        return df
    except Exception as err:
        print(f":: Error on convert_timezone {field}:", err)
        return df
    finally:
        try:
            df.drop(['timezone_obj'], axis=1, inplace=True)
        except Exception as e:
            print(
                f"Convert Timezone: Error dropping timezone_obj column: {e}"
            )


def add_timestamp_to_time(df: pandas.DataFrame, field: str, date: str, time: str):
    """
    Takes a pandas DataFrame and combines the values from a date column and a time column
    to create a new timestamp column.

    :param df: pandas DataFrame to be modified.
    :param field: Name of the new column to store the combined timestamp.
    :param date: Name of the column in the df DataFrame containing date values.
    :param time: Name of the column in the df DataFrame containing time values.
    :return: Modified pandas DataFrame with the combined timestamp stored in a new column.
    """
    try:
        df[field] = pandas.to_datetime(df[date].astype(str) + " " + df[time].astype(str))
    except Exception as e:
        print(f"Error adding timestamp to time: {str(e)}")
        return df
    return df
