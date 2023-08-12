from datetime import datetime, timedelta
from typing import List

import numpy as np
from pandas import DataFrame, concat, to_datetime
from gps2gtfs.data_field.im_field import ExtractedStopField, StopTimeField
from gps2gtfs.utility.logger import logger


def extract_stop_features(stops: DataFrame) -> DataFrame:
    stop_times_df = calculate_stop_times(stops)
    add_features_from_datetimes(stop_times_df)
    return stop_times_df


def calculate_stop_times(stops_df: DataFrame) -> DataFrame:
    # Drop records with End terminals
    terminals: List[str] = stops_df[ExtractedStopField.BUS_STOP.value].unique().tolist()
    stops_df.drop(
        stops_df[stops_df[ExtractedStopField.BUS_STOP.value] == terminals[0]].index,
        inplace=True,
    )
    stops_df.drop(
        stops_df[stops_df[ExtractedStopField.BUS_STOP.value] == terminals[1]].index,
        inplace=True,
    )

    logger.info("Preparing to extract stop details")

    # grouping all records filtered for every stop
    stops_df[ExtractedStopField.GROUPED_ENDS.value] = (
        (
            stops_df[ExtractedStopField.BUS_STOP.value].shift()
            != stops_df[ExtractedStopField.BUS_STOP.value]
        )
    ).cumsum()

    # creating a new dataframe for stop times
    columns = [
        StopTimeField.TRIP_ID.value,
        StopTimeField.DEVICE_ID.value,
        StopTimeField.DATE.value,
        StopTimeField.DIRECTION.value,
        StopTimeField.BUS_STOP.value,
        StopTimeField.ARRIVAL_TIME.value,
        StopTimeField.DEPARTURE_TIME.value,
        StopTimeField.DWELL_TIME.value,
    ]
    stop_times_df = DataFrame(columns=columns)

    # Loop over every grouped filtered records and
    # choose the two records that indicate arrival and departure to the stop
    for _, group in stops_df.groupby(ExtractedStopField.GROUPED_ENDS.value):
        values = []
        trip_id = np.unique(group[ExtractedStopField.TRIP_ID.value].values)[0]
        direction = np.unique(group[ExtractedStopField.DIRECTION.value].values)[0]
        deviceid = np.unique(group[ExtractedStopField.DEVICE_ID.value].values)[0]
        date = np.unique(group[ExtractedStopField.DATE.value].values)[0]
        bus_stop = np.unique(group[ExtractedStopField.BUS_STOP.value].values)[0]

        if 0 in group[ExtractedStopField.SPEED.value].values:
            arrival_time = group[group[ExtractedStopField.SPEED.value] == 0][
                ExtractedStopField.TIME.value
            ].min()
            buffer_leaving_time = group[ExtractedStopField.TIME.value].max()
            rough_departure_time = group[group[ExtractedStopField.SPEED.value] == 0][
                ExtractedStopField.TIME.value
            ].max()
            departure_time = calculate_departure_time(
                rough_departure_time, buffer_leaving_time, date
            )
        else:
            arrival_time = group[ExtractedStopField.TIME.value].min()
            departure_time = arrival_time

        values.extend(
            [
                trip_id,
                deviceid,
                date,
                direction,
                bus_stop,
                arrival_time,
                departure_time,
                None,
            ]
        )
        new_row = DataFrame([values], columns=columns)
        stop_times_df = concat([stop_times_df, new_row], ignore_index=True)
        # stop_times_df = stop_times_df.append(dict(zip(columns, values)), ignore_index=True)

    for i in range(len(stop_times_df)):
        stop_times_df.at[i, StopTimeField.DWELL_TIME.value] = datetime.combine(
            date.min, stop_times_df.at[i, StopTimeField.DEPARTURE_TIME.value]
        ) - datetime.combine(
            date.min, stop_times_df.at[i, StopTimeField.ARRIVAL_TIME.value]
        )

    stop_times_df[StopTimeField.DWELL_TIME_IN_SECONDS.value] = stop_times_df[
        StopTimeField.DWELL_TIME.value
    ] / np.timedelta64(1, "s")

    logger.info("Successfully extracted stop related features")
    return stop_times_df


def add_features_from_datetimes(stop_times_df: DataFrame) -> None:
    # bus_stop_times = bus_stop_times.drop(bus_stop_times[bus_stop_times['dwell_time_in_seconds']>threshold].index)

    stop_times_df[StopTimeField.DAY_OF_WEEK.value] = to_datetime(
        stop_times_df[StopTimeField.DATE.value]
    ).dt.weekday
    stop_times_df[StopTimeField.HOUR_OF_DAY.value] = list(
        map(lambda x: x.hour, (stop_times_df[StopTimeField.ARRIVAL_TIME.value]))
    )
    stop_times_df[StopTimeField.IS_WEEKDAY.value] = list(
        map(
            lambda x: 1 if x < 5 else 0,
            (stop_times_df[StopTimeField.DAY_OF_WEEK.value]),
        )
    )


def calculate_departure_time(rough_departure_time, buffer_leaving_time, date):
    if (
        datetime.combine(date, buffer_leaving_time)
        - datetime.combine(date, rough_departure_time)
    ).total_seconds() > 15:
        return (
            datetime.combine(date, rough_departure_time) + timedelta(seconds=15)
        ).time()
    else:
        return buffer_leaving_time
