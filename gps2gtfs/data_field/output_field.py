from enum import Enum


class TripField(Enum):
    DEVICE_ID = "deviceid"
    DATE = "date"
    TRIP_ID = "trip_id"

    END_TIME = "end_time"
    END_TERMINAL = "end_terminal"
    START_TIME = "start_time"
    START_TERMINAL = "start_terminal"
    DIRECTION = "direction"
    DURATION = "duration"
    DURATION_IN_MINS = "duration_in_mins"
    DAY_OF_WEEK = "day_of_week"
    HOUR_OF_DAY = "hour_of_day"


class StopTimeField(Enum):
    TRIP_ID = "trip_id"
    DEVICE_ID = "deviceid"
    DATE = "date"
    DIRECTION = "direction"
    BUS_STOP = "bus_stop"
    ARRIVAL_TIME = "arrival_time"
    DEPARTURE_TIME = "departure_time"
    DWELL_TIME = "dwell_time"
    DWELL_TIME_IN_SECONDS = "dwell_time_in_seconds"
    DAY_OF_WEEK = "day_of_week"
    HOUR_OF_DAY = "hour_of_day"
    IS_WEEKDAY = "is_weekday"
