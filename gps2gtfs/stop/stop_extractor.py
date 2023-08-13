from typing import Tuple
from multiprocessing import Pool, cpu_count

from geopandas import GeoDataFrame
from pandas import DataFrame, concat
from gps2gtfs.data_field.im_field import TrajectoryField
from gps2gtfs.data_field.input_field import StopField
from gps2gtfs.utility.logger import logger


def extract_stops(
    trajectory_df: DataFrame,
    direction1_stops_buffer: GeoDataFrame,
    direction2_stops_buffer: GeoDataFrame,
    direction1_stops_extended_buffer: GeoDataFrame,
    direction2_stops_extended_buffer: GeoDataFrame,
) -> DataFrame:
    logger.info("Preparing to extract stops from GPS Data")
    # project to local coordinate system before buffer filtering
    trajectory_df = trajectory_df.to_crs("EPSG:5234")

    # split trajectories by direction
    direction1_trajectory = trajectory_df[
        trajectory_df[TrajectoryField.DIRECTION.value] == 1
    ]
    direction2_trajectory = trajectory_df[
        trajectory_df[TrajectoryField.DIRECTION.value] == 2
    ]

    # reset index before for loop
    direction1_trajectory.reset_index(drop=True, inplace=True)
    direction2_trajectory.reset_index(drop=True, inplace=True)

    # filter records within stops buffer of both directions
    direction1_trajectory = match_gps_data_with_stops(
        direction1_trajectory, direction1_stops_buffer, direction1_stops_extended_buffer
    )
    direction2_trajectory = match_gps_data_with_stops(
        direction2_trajectory, direction2_stops_buffer, direction2_stops_extended_buffer
    )

    # concatenate dataframes of both directions and keep only records filtered within stops
    trip_all_points = concat([direction1_trajectory, direction2_trajectory])
    stops = trip_all_points.dropna()

    logger.info("Successfully Extracted Stops")
    return stops


def match_gps_data_with_stops(
    trajectory_df: DataFrame,
    stops_buffer_geo_df: GeoDataFrame,
    stops_extended_buffer_geo_df: GeoDataFrame,
) -> DataFrame:
    logger.info("Preparing to match stops coordinates with GPS Data Points")
    num_processes = cpu_count()  # Number of available CPU cores
    chunk_size = len(trajectory_df) // num_processes
    chunks = [
        (
            trajectory_df[i : i + chunk_size],
            stops_buffer_geo_df,
            stops_extended_buffer_geo_df,
        )
        for i in range(0, len(trajectory_df), chunk_size)
    ]

    logger.info("Starting to match stops coordinates with GPS Data Points")
    with Pool(processes=num_processes) as pool:
        updated_chunks = pool.map(match_gps_points, chunks)

    logger.info("Successfully matched stops coordinates with GPS Data Points")
    return concat(updated_chunks, ignore_index=True)


def match_gps_points(args: Tuple) -> DataFrame:
    trajectory_df, stops_buffer_geo_df, stops_extended_buffer_geo_df = args

    for i in range(len(trajectory_df)):
        for stop in range(len(stops_buffer_geo_df)):
            if stops_buffer_geo_df.iloc[stop].geometry.contains(
                trajectory_df.iloc[i].geometry
            ):
                trajectory_df.at[
                    i, TrajectoryField.BUS_STOP.value
                ] = stops_buffer_geo_df.at[stop, StopField.STOP_ID.value]
                break
            elif stops_extended_buffer_geo_df.iloc[stop].geometry.contains(
                trajectory_df.iloc[i].geometry
            ):
                trajectory_df.at[
                    i, TrajectoryField.BUS_STOP.value
                ] = stops_extended_buffer_geo_df.at[stop, StopField.STOP_ID.value]
                break

    return trajectory_df
