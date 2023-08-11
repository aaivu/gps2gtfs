from multiprocessing import Pool, cpu_count
from typing import Tuple

from geopandas import GeoDataFrame
from pandas import DataFrame, Series, concat
from gps2gtfs.data_field.im_field import TerminalGPSField
from gps2gtfs.data_field.input_field import TerminalField
from gps2gtfs.utility.data_io_converter import (
    extend_geo_buffer,
    pandas_to_geo_data_frame,
)

TERMINAL_ENTRY = "1"
TERMINAL_EXIT = "0"


def extract_trips(
    raw_gps_df: DataFrame,
    trip_terminals_df: DataFrame,
    buffer_radius: int,
) -> DataFrame:
    # Converting to GeoDataframe
    raw_gps_geo_df = pandas_to_geo_data_frame(raw_gps_df)
    trip_terminals_geo_df = pandas_to_geo_data_frame(trip_terminals_df)

    # Splitting the GPS data into chunks to be processed in parallel
    num_processes = cpu_count()  # Number of available CPU cores
    chunk_size = len(raw_gps_geo_df) // num_processes
    chunks = [
        (raw_gps_geo_df[i : (i + chunk_size)], trip_terminals_geo_df, buffer_radius)
        for i in range(0, len(raw_gps_geo_df), chunk_size)
    ]

    with Pool(processes=num_processes) as pool:
        updated_chunks = pool.map(match_raw_gps_data_with_terminals, chunks)

    raw_gps_data_with_terminals: DataFrame = concat(updated_chunks, ignore_index=True)
    gps_data_within_terminal_buffer = (
        raw_gps_data_with_terminals.dropna()
    )  # Filtering records within terminal buffer

    # EXTRACTING TRIP ENDS
    trip_terminals_gps_data = extract_trip_terminals(gps_data_within_terminal_buffer)

    # Providing unique trip id for trips which have entry / exit values within the 2 end terminals
    return terminals_gps_data_to_trips(trip_terminals_gps_data)


def match_raw_gps_data_with_terminals(args: Tuple) -> GeoDataFrame:
    raw_gps_geo_df, trip_terminals_geo_df, buffer_radius = args

    # Creating buffer area to extract records around trip terminals
    trip_terminals_buffer = extend_geo_buffer(trip_terminals_geo_df, buffer_radius)

    # Filtering coordinates within trip terminals end buffer
    raw_gps_geo_df[TerminalGPSField.BUS_STOP.value] = Series(
        dtype="object"
    )  # Creating a new column in raw gps data set
    raw_gps_geo_df.reset_index(
        drop=True, inplace=True
    )  # Resetting indices to run a for loop

    for i in range(len(raw_gps_geo_df)):
        for stop in range(len(trip_terminals_geo_df)):
            if trip_terminals_buffer.iloc[stop].geometry.contains(
                raw_gps_geo_df.iloc[i].geometry
            ):
                raw_gps_geo_df.at[
                    i, TerminalGPSField.BUS_STOP.value
                ] = trip_terminals_geo_df.at[stop, TerminalField.TERMINAL_ID.value]
                break
    return raw_gps_geo_df


def extract_trip_terminals(gps_data_within_terminal_buffer: DataFrame) -> DataFrame:
    # Grouping the filtered records of one trip terminal and one date
    gps_data_within_terminal_buffer[TerminalGPSField.GROUPED_TERMINALS.value] = (
        (
            gps_data_within_terminal_buffer[TerminalGPSField.BUS_STOP.value].shift()
            != gps_data_within_terminal_buffer[TerminalGPSField.BUS_STOP.value]
        )
        | (
            gps_data_within_terminal_buffer[TerminalGPSField.DATE.value].shift()
            != gps_data_within_terminal_buffer[TerminalGPSField.DATE.value]
        )
    ).cumsum()

    # Finding only the entry or exit record of the terminals
    # Early records is the entry(1) to the terminal and last record as the exit(0) to the end terminal
    gps_data_within_terminal_buffer[TerminalGPSField.ENTRY_EXIT.value] = Series(
        dtype="object"
    )
    gps_data_within_terminal_buffer.reset_index(drop=True, inplace=True)

    # Finding rows corresponding to maximum and minimum 'devicetime' in each group
    max_devicetime_rows = gps_data_within_terminal_buffer.groupby(
        TerminalGPSField.GROUPED_TERMINALS.value
    )[TerminalGPSField.DEVICE_TIME.value].idxmax()

    min_devicetime_rows = gps_data_within_terminal_buffer.groupby(
        TerminalGPSField.GROUPED_TERMINALS.value
    )[TerminalGPSField.DEVICE_TIME.value].idxmin()

    # Setting 'entry/exit' column based on max and min 'devicetime' rows for each group
    gps_data_within_terminal_buffer.loc[
        max_devicetime_rows, TerminalGPSField.ENTRY_EXIT.value
    ] = TERMINAL_EXIT

    gps_data_within_terminal_buffer.loc[
        min_devicetime_rows, TerminalGPSField.ENTRY_EXIT.value
    ] = TERMINAL_ENTRY

    # Dropping rows with NaN values in 'entry/exit' column (if any)
    trip_terminals_gps_data = gps_data_within_terminal_buffer.dropna(
        subset=[TerminalGPSField.ENTRY_EXIT.value]
    ).reset_index(drop=True)

    return trip_terminals_gps_data


def terminals_gps_data_to_trips(trip_terminals_gps_data: DataFrame) -> DataFrame:
    trip = 0
    for i in range(len(trip_terminals_gps_data) - 1):
        if (
            trip_terminals_gps_data.at[i, TerminalGPSField.BUS_STOP.value]
            != trip_terminals_gps_data.at[i + 1, TerminalGPSField.BUS_STOP.value]
        ) & (
            trip_terminals_gps_data.at[i, TerminalGPSField.DATE.value]
            == trip_terminals_gps_data.at[i + 1, TerminalGPSField.DATE.value]
        ):
            trip += 1
            trip_terminals_gps_data.at[i, TerminalGPSField.TRIP_ID.value] = trip
            trip_terminals_gps_data.at[i + 1, TerminalGPSField.TRIP_ID.value] = trip

    trips = trip_terminals_gps_data.dropna()
    trips = trips.groupby(TerminalGPSField.TRIP_ID.value).filter(
        lambda x: len(x) > 1
    )  # Removing outliers where no defined 2 trip terminals for a trip
    trips.reset_index(drop=True, inplace=True)

    return trips
