from pandas import DataFrame, to_datetime

from gps2gtfs.data_field.im_field import CleanedRawGPSField
from gps2gtfs.data_field.input_field import RawGPSField


def clean(raw_gps_df: DataFrame) -> DataFrame:
    """
    Clean and preprocess a DataFrame containing raw GPS data.

    The function takes a pandas DataFrame with raw GPS data and performs the following cleaning
    and preprocessing steps:

    1. Removes the rows where latitude and longitude are both zero.
    2. Converts the 'DEVICE_TIME' column to pandas datetime format.
    3. Extracts the date and time components from the 'DEVICE_TIME' column and adds them as new
       columns.
    4. Sorts the DataFrame by 'DEVICE_ID', 'DATE', and 'TIME' in ascending order.

    Parameters:
        raw_gps_df (DataFrame): A pandas DataFrame containing raw GPS data.

    Returns:
        DataFrame: A new DataFrame with the cleaned and preprocessed GPS data.

    Example:
        >>> import pandas as pd

        >>> data = {
        ...     'DEVICE_ID': [1, 2, 3],
        ...     'LATITUDE': [37.7749, 40.7486, 0],
        ...     'LONGITUDE': [-122.4194, -73.9857, 0],
        ...     'DEVICE_TIME': ['2023-07-27 12:34:56', '2023-07-27 10:20:30', '2023-07-27 09:15:00']
        ... }
        >>> raw_gps_df = pd.DataFrame(data)
        >>> cleaned_gps_df = clean(raw_gps_df)
        >>> print(cleaned_gps_df)
           DEVICE_ID  LATITUDE  LONGITUDE        DEVICE_TIME        DATE      TIME
        1         2   40.7486   -73.9857 2023-07-27 10:20:30  2023-07-27  10:20:30
        0         1   37.7749  -122.4194 2023-07-27 12:34:56  2023-07-27  12:34:56
    """
    cleaned_raw_gps_df = raw_gps_df[
        (raw_gps_df[RawGPSField.LATITUDE.value] != 0)
        & (raw_gps_df[RawGPSField.LONGITUDE.value] != 0)
    ].copy()

    cleaned_raw_gps_df[RawGPSField.DEVICE_TIME.value] = to_datetime(
        cleaned_raw_gps_df[RawGPSField.DEVICE_TIME.value]
    )
    cleaned_raw_gps_df[CleanedRawGPSField.DATE.value] = cleaned_raw_gps_df[
        RawGPSField.DEVICE_TIME.value
    ].dt.date
    cleaned_raw_gps_df[CleanedRawGPSField.TIME.value] = cleaned_raw_gps_df[
        RawGPSField.DEVICE_TIME.value
    ].dt.time

    cleaned_raw_gps_df.sort_values(
        by=[
            RawGPSField.DEVICE_ID.value,
            CleanedRawGPSField.DATE.value,
            CleanedRawGPSField.TIME.value,
        ],
        inplace=True,
    )

    return cleaned_raw_gps_df
