from typing import Dict, List, Optional

from pandas import DataFrame
from gps2gtfs.data_field.im_field import (
    ProcessedGPSField,
    TripField,
)
from gps2gtfs.data_field.input_field import RawGPSField, StopField, TerminalField
from gps2gtfs.utility.data_io_converter import read_csv_file
from gps2gtfs.utility.logger import logger


def load(file_paths: Dict[str, str]) -> List[Optional[DataFrame]]:
    """
    Load multiple CSV files into a list of pandas DataFrames.

    The function takes a dictionary of file names as keys and their corresponding file paths as
    values. It reads each CSV file using the `read_csv_file` function and returns a list of pandas
    DataFrames. If a file is not found or there is an error during file reading, the respective
    DataFrame in the returned list will be set to None.

    Parameters:
        file_paths (Dict[str, str]): A dictionary mapping file names to their file paths.

    Returns:
        List[Optional[DataFrame]]: A list containing pandas DataFrames read from the provided
                                   CSV files. If a file is not found or there is an error during
                                   file reading, the corresponding element in the list will be None.

    Notes:
        - The function uses the `read_csv_file` function to read each CSV file.
        - The order of DataFrames in the returned list corresponds to the order of file names in
          the dictionary keys.

    Example:
        >>> file_paths = {
        ...     "data1.csv": "path/to/data1.csv",
        ...     "data2.csv": "path/to/data2.csv",
        ...     "data3.csv": "path/to/data3.csv"
        ... }
        >>> data_frames = load(file_paths)
        >>> for file_name, df in zip(file_paths.keys(), data_frames):
        ...     if df is not None:
        ...         print(f"Contents of {file_name}:")
        ...         print(df.head())
        ...     else:
        ...         print(f"Error occurred while reading {file_name}.")
    """
    return [read_csv_file(path, file_name) for file_name, path in file_paths.items()]


def load_data_for_pipeline(
    raw_gps_data_path: str,
    trip_terminals_data_path: str,
    stops_data_path: str,
) -> Optional[List[DataFrame]]:
    """
    Load and validate data for a processing pipeline.

    This function loads data from specified CSV files for a processing pipeline that involves raw GPS
    data, trip terminals data, and stops data. It performs validation to ensure that the loaded data
    contains the required columns.

    Parameters:
        raw_gps_data_path (str): File path to the CSV containing raw GPS data.
        trip_terminals_data_path (str): File path to the CSV containing trip terminals data.
        stops_data_path (str): File path to the CSV containing stops data.

    Returns:
        Optional[List[DataFrame]]: A list of pandas DataFrames containing the loaded data. If any
                                   data file is not found or does not contain the required columns,
                                   None is returned.

    Notes:
        - The function uses the 'load' function to load data from the specified file paths.
        - It validates that the loaded DataFrames contain the required columns for raw GPS data,
          trip terminals data, and stops data.
        - If the data passes validation, a list containing the loaded DataFrames is returned.
        - If any data file is missing or contains incorrect columns, an error message is printed,
          and None is returned.

    Example:
        >>> raw_gps_path = "path/to/raw_gps_data.csv"
        >>> trip_terminals_path = "path/to/trip_terminals_data.csv"
        >>> stops_path = "path/to/stops_data.csv"
        >>> data_frames = load_data_for_pipeline(raw_gps_path, trip_terminals_path, stops_path)
        >>> if data_frames is not None:
        ...     # Proceed with the processing pipeline using the loaded data
        ... else:
        ...     print("Data loading and validation failed.")
    """
    file_paths = {
        "Raw GPS data": raw_gps_data_path,
        "Trip terminals data": trip_terminals_data_path,
        "Stops data": stops_data_path,
    }

    raw_gps_df, trip_terminals_df, stops_df = load(file_paths)
    if not any([df is None for df in [raw_gps_df, trip_terminals_df, stops_df]]):
        raw_gps_fields = {f.value for f in RawGPSField}
        trip_terminals_fields = {f.value for f in TerminalField}
        stops_fields = {f.value for f in StopField}
        if (
            (not raw_gps_fields - set(raw_gps_df.columns.values))
            and (not trip_terminals_fields - set(trip_terminals_df.columns.values))
            and (not stops_fields - set(stops_df.columns.values))
        ):
            logger.info("Data Loaded successfully for pipeline")
            return [raw_gps_df, trip_terminals_df, stops_df]
        else:
            logger.error("Failed to load data for pipeline")
            logger.error("Following columns should be included in your CSV files,")
            logger.error(f"In Raw GPS data: {raw_gps_fields}")
            logger.error(f"In Trip terminals data: {trip_terminals_fields}")
            logger.error(f"In Stops data: {stops_fields}")


def load_data_for_trip_calculation(
    raw_gps_data_path: str,
    trip_terminals_data_path: str,
) -> Optional[List[DataFrame]]:
    file_paths = {
        "Raw GPS data": raw_gps_data_path,
        "Trip terminals data": trip_terminals_data_path,
    }

    raw_gps_df, trip_terminals_df = load(file_paths)
    if not any([df is None for df in [raw_gps_df, trip_terminals_df]]):
        raw_gps_fields = {f.value for f in RawGPSField}
        trip_terminals_fields = {f.value for f in TerminalField}
        if (not raw_gps_fields - set(raw_gps_df.columns.values)) and (
            not trip_terminals_fields - set(trip_terminals_df.columns.values)
        ):
            logger.info("Data loaded successfully for trip calculation")
            return [raw_gps_df, trip_terminals_df]
        else:
            logger.error("Failed to load Data for trip calculation")
            logger.error("Following columns should be included in your CSV files,")
            logger.error(f"In Raw GPS data: {raw_gps_fields}")
            logger.error(f"In Trip terminals data: {trip_terminals_fields}")


def load_data_for_stop_calculation(
    raw_gps_data_path: str,
    processed_gps_data_path: str,
    trips_data_path: str,
    stops_data_path: str,
) -> Optional[List[DataFrame]]:
    file_paths = {
        "Raw GPS data": raw_gps_data_path,
        "Processed GPS data": processed_gps_data_path,
        "Trips data": trips_data_path,
        "Stops data": stops_data_path,
    }

    raw_gps_df, processed_gps_df, trips_df, stops_df = load(file_paths)
    if not any(
        [df is None for df in [raw_gps_df, processed_gps_df, trips_df, stops_df]]
    ):
        raw_gps_fields = {f.value for f in RawGPSField}
        processed_gps_fields = {f.value for f in ProcessedGPSField}
        trips_fields = {f.value for f in TripField}
        stops_fields = {f.value for f in StopField}
        if (
            (not raw_gps_fields - set(raw_gps_df.columns.values))
            and (not processed_gps_fields - set(processed_gps_df.columns.values))
            and (not trips_fields - set(trips_df.columns.values))
            and (not stops_fields - set(stops_df.columns.values))
        ):
            logger.info("Data loaded successfully for stop calculation")
            return [raw_gps_df, processed_gps_df, trips_df, stops_df]
        else:
            logger.error("Following columns should be included in your CSV files,")
            logger.error(f"In Raw GPS data: {raw_gps_fields}")
            logger.error(f"In Processed GPS data: {processed_gps_fields}")
            logger.error(f"In Trips data: {trips_fields}")
            logger.error(f"In Stops data: {stops_fields}")
