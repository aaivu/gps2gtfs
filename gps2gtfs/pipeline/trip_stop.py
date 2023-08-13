import warnings

from pandas.errors import SettingWithCopyWarning
from gps2gtfs.load_data.load_from_csv import load_data_for_trip_stop_pipeline
from gps2gtfs.preprocessing.data_cleaner import clean
from gps2gtfs.stop.data_preparator import create_stop_buffers, prepare_trajectory_df
from gps2gtfs.stop.feature_extractor import extract_stop_features
from gps2gtfs.stop.stop_extractor import extract_stops
from gps2gtfs.trip.feature_extractor import extract_trip_features
from gps2gtfs.trip.trip_extractor import extract_trips
from gps2gtfs.utility.data_io_converter import write_as_csv_file
from gps2gtfs.utility.logger import logger


def run(
    raw_gps_data_path: str,
    trip_terminals_data_path: str,
    stops_data_path: str,
    terminals_buffer_radius: int,
    stops_buffer_radius: int,
    stops_extended_buffer_radius: int,
) -> None:
    # Suppress the SettingWithCopyWarning
    warnings.filterwarnings("ignore", category=SettingWithCopyWarning)

    logger.info("Pipeline method called !")
    logger.info("Starting Pipeline for extracting Trip Data")
    loaded_data = load_data_for_trip_stop_pipeline(
        raw_gps_data_path, trip_terminals_data_path, stops_data_path
    )
    if loaded_data:
        logger.info("Successfully read the data")
        raw_gps_df, trip_terminals_df, stops_df = loaded_data

        cleaned_raw_gps_df = clean(raw_gps_df)

        trips_df = extract_trips(
            cleaned_raw_gps_df, trip_terminals_df, terminals_buffer_radius
        )

        trip_features_df = extract_trip_features(trips_df)

        logger.info("Finished extracting Trip Data")
        logger.info("Starting Pipeline for extracting Bus Stop Data")

        logger.info("Preparing data for calculations regarding bus stops")
        (
            raw_gps_geo_df,
            direction1_stops_buffer,
            direction2_stops_buffer,
            direction1_stops_extended_buffer,
            direction2_stops_extended_buffer,
        ) = create_stop_buffers(
            cleaned_raw_gps_df,
            stops_df,
            stops_buffer_radius,
            stops_extended_buffer_radius,
        )

        trajectory_df = prepare_trajectory_df(
            raw_gps_geo_df, trips_df, trip_features_df
        )

        stop_gps_df = extract_stops(
            trajectory_df,
            direction1_stops_buffer,
            direction2_stops_buffer,
            direction1_stops_extended_buffer,
            direction2_stops_extended_buffer,
        )

        stop_times_df = extract_stop_features(stop_gps_df)

        write_as_csv_file(trip_features_df, "trips.csv")
        write_as_csv_file(stop_times_df, "stops.csv")

        logger.info("Pipeline finished successfully !")
