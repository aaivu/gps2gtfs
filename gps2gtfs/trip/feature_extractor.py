from datetime import date, datetime
from typing import List

from numpy import ndarray, select, timedelta64
from pandas import DataFrame, Series, to_datetime
from gps2gtfs.data_field.im_field import TerminalGPSField, TripField
from gps2gtfs.utility.logger import logger


def extract_trip_features(trips: DataFrame) -> DataFrame:
    logger.info("Starting to extracting features for the trips")
    trips = trips.copy()
    add_end_time_and_end_terminal(trips)
    trips = trips.iloc[::2]

    trips = trips.drop(
        [
            TerminalGPSField.ID.value,
            TerminalGPSField.DEVICE_TIME.value,
            TerminalGPSField.LATITUDE.value,
            TerminalGPSField.LONGITUDE.value,
            TerminalGPSField.SPEED.value,
            TerminalGPSField.GEOMETRY.value,
            TerminalGPSField.GROUPED_TERMINALS.value,
            TerminalGPSField.ENTRY_EXIT.value,
        ],
        axis=1,
    )

    trips.insert(0, TripField.TRIP_ID.value, trips.pop(TripField.TRIP_ID.value))
    trips.rename(
        columns={
            TerminalGPSField.TIME.value: TripField.START_TIME.value,
            TerminalGPSField.BUS_STOP.value: TripField.START_TERMINAL.value,
        },
        inplace=True,
    )

    trips[TripField.DIRECTION.value] = find_direction(trips)

    trips = trips[
        [
            TripField.TRIP_ID.value,
            TripField.DEVICE_ID.value,
            TripField.DATE.value,
            TripField.START_TERMINAL.value,
            TripField.END_TERMINAL.value,
            TripField.DIRECTION.value,
            TripField.START_TIME.value,
            TripField.END_TIME.value,
        ]
    ].reset_index(drop=True)

    # Calculating trip duration and adding it into the trips dataset
    add_trip_duration(trips)

    trips[TripField.DAY_OF_WEEK.value] = find_day_of_week(trips)
    trips[TripField.HOUR_OF_DAY.value] = find_hour_of_day(trips)

    logger.info("Successfully extracted features for the trips")
    return trips


def add_end_time_and_end_terminal(trips: DataFrame) -> None:
    trips[[TripField.END_TIME.value, TripField.END_TERMINAL.value]] = trips[
        [TerminalGPSField.TIME.value, TerminalGPSField.BUS_STOP.value]
    ].shift(-1)
    logger.info("Added End Time & End Terminal Details")


def find_direction(trips: DataFrame) -> ndarray:
    logger.info("Finding Direction data for the trips")
    terminals: List[str] = trips[TripField.START_TERMINAL.value].unique().tolist()
    conditions = [
        (trips[TripField.START_TERMINAL.value] == terminals[0]),
        (trips[TripField.START_TERMINAL.value] == terminals[1]),
    ]
    values = [1, 2]

    return select(conditions, values)


def add_trip_duration(trips: DataFrame) -> None:
    trips[TripField.DURATION.value] = Series(dtype="object")
    for i in range(len(trips)):
        trips.at[i, TripField.DURATION.value] = datetime.combine(
            date.min, trips.at[i, TripField.END_TIME.value]
        ) - datetime.combine(date.min, trips.at[i, TripField.START_TIME.value])

    trips[TripField.DURATION_IN_MINS.value] = trips[
        TripField.DURATION.value
    ] / timedelta64(1, "m")
    logger.info("Extracted Trip Duration")


def find_day_of_week(trips: DataFrame) -> Series:
    return to_datetime(trips[TripField.DATE.value]).dt.weekday


def find_hour_of_day(trips: DataFrame) -> List:
    return list(map(lambda x: x.hour, (trips[TripField.START_TIME.value])))
