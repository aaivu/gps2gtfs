from gps2gtfs.load_data.load_from_csv import load_data_for_trip_pipeline
from gps2gtfs.preprocessing.data_cleaner import clean
from gps2gtfs.trip.feature_extractor import extract_trip_features
from gps2gtfs.trip.trip_extractor import extract_trips
from gps2gtfs.utility.data_io_converter import write_as_csv_file
from gps2gtfs.utility.logger import logger


def run(
        raw_gps_data_path: str,
        trip_terminals_data_path: str,
        terminals_buffer_radius: int,
):
    logger.info("Pipeline method called !")
    logger.info("Starting Pipeline for extracting Trip Data")
    loaded_data = load_data_for_trip_pipeline(
        raw_gps_data_path, trip_terminals_data_path
    )
    if loaded_data:
        logger.info("Successfully read the data")
        raw_gps_df, trip_terminals_df = loaded_data

        cleaned_raw_gps_df = clean(raw_gps_df)

        trips_df = extract_trips(
            cleaned_raw_gps_df, trip_terminals_df, terminals_buffer_radius
        )

        trip_features_df = extract_trip_features(trips_df)

        logger.info("Finished extracting Trip Data")

        write_as_csv_file(trip_features_df, "trips.csv")

        logger.info("Pipeline finished successfully !")
