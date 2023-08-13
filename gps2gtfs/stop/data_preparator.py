from typing import List, Tuple

from geopandas import GeoDataFrame
from pandas import DataFrame, merge
from gps2gtfs.data_field.im_field import (
    CleanedRawGPSField,
    ProcessedGPSField,
    TrajectoryField,
)
from gps2gtfs.data_field.output_field import TripField
from gps2gtfs.data_field.input_field import StopField
from gps2gtfs.utility.data_io_converter import (
    extend_geo_buffer,
    pandas_to_geo_data_frame,
)
from gps2gtfs.utility.logger import logger


def create_stop_buffers(
    raw_gps_df: DataFrame,
    stops_df: DataFrame,
    buffer_radius: int,
    extended_buffer_radius: int,
) -> Tuple:
    logger.info("Splitting stops dataframe into two based on route direction")
    raw_gps_geo_df = pandas_to_geo_data_frame(raw_gps_df)
    stops_geo_df = pandas_to_geo_data_frame(stops_df)

    logger.info("Splitting stops dataframe into two based on route direction")
    directions: List[str] = stops_geo_df[StopField.DIRECTION.value].unique().tolist()
    directions = list(filter(lambda d: not d.isdigit(), directions))
    direction1_stops_geo_df = stops_geo_df[
        stops_geo_df[StopField.DIRECTION.value] == directions[0]
    ]
    direction2_stops_geo_df = stops_geo_df[
        stops_geo_df[StopField.DIRECTION.value] == directions[1]
    ]

    direction2_stops_geo_df.reset_index(drop=True, inplace=True)

    # proximity analysis
    # creating a buffer
    direction1_stops_buffer = extend_geo_buffer(direction1_stops_geo_df, buffer_radius)
    direction2_stops_buffer = extend_geo_buffer(direction2_stops_geo_df, buffer_radius)

    logger.info("Forming GEO Buffer Area to capture data points around bus stop")
    # creating additional extra buffer to accommodate points if they were missed in standard stop buffer
    direction1_stops_extended_buffer = extend_geo_buffer(
        direction1_stops_geo_df, extended_buffer_radius
    )
    direction2_stops_extended_buffer = extend_geo_buffer(
        direction2_stops_geo_df, extended_buffer_radius
    )

    return (
        raw_gps_geo_df,
        direction1_stops_buffer,
        direction2_stops_buffer,
        direction1_stops_extended_buffer,
        direction2_stops_extended_buffer,
    )


def prepare_trajectory_df(
    raw_gps_geo_df: GeoDataFrame,
    processed_gps_df: DataFrame,
    trips_df: DataFrame,
) -> DataFrame:
    logger.info("Preparing to add Trip Details to GPS Data")
    # gps records that are matched with end terminals, are merged with whole GPS records
    processed_gps_df = processed_gps_df[
        [
            ProcessedGPSField.ID.value,
            ProcessedGPSField.BUS_STOP.value,
            ProcessedGPSField.TRIP_ID.value,
        ]
    ]
    trajectory_df = merge(
        left=raw_gps_geo_df,
        right=processed_gps_df,
        how="outer",
        left_on=CleanedRawGPSField.ID.value,
        right_on=ProcessedGPSField.ID.value,
    )

    # gps records that are not associated with the terminals are assigned as trip id = 0
    trajectory_df[TrajectoryField.TRIP_ID.value].fillna(0, inplace=True)

    # run a loop to assign trip_id to records that are in between the terminals
    trajectory_df.reset_index(drop=True, inplace=True)

    trip = 1
    for i in range(len(trajectory_df) - 1):
        if trajectory_df.at[i, TrajectoryField.TRIP_ID.value] == trip:
            if trajectory_df.at[i + 1, TrajectoryField.TRIP_ID.value] == 0:
                trajectory_df.at[i + 1, TrajectoryField.TRIP_ID.value] = trip
            elif trajectory_df.at[i + 1, TrajectoryField.TRIP_ID.value] == trip:
                trip = trip + 1

    trajectory_df.drop(
        trajectory_df[trajectory_df[TrajectoryField.TRIP_ID.value] == 0].index,
        inplace=True,
    )  # drop records that are not identified as a trip

    # Identify the directions of each trajectory using trips extracted data
    directions = trips_df.set_index(TripField.TRIP_ID.value).to_dict()[
        TripField.DIRECTION.value
    ]
    trajectory_df[TrajectoryField.DIRECTION.value] = list(
        map(
            lambda trip_id: directions[trip_id],
            trajectory_df[TrajectoryField.TRIP_ID.value],
        )
    )

    logger.info("Successfully added Trip Details to GPS Data")
    return trajectory_df
