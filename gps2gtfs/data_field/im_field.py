from enum import Enum


class CleanedRawGPSField(Enum):
    ID = "id"
    DEVICE_ID = "deviceid"
    LATITUDE = "latitude"
    LONGITUDE = "longitude"
    DEVICE_TIME = "devicetime"
    SPEED = "speed"

    DATE = "date"
    TIME = "time"


class TerminalGPSField(Enum):
    ID = "id"
    DEVICE_ID = "deviceid"
    LATITUDE = "latitude"
    LONGITUDE = "longitude"
    DEVICE_TIME = "devicetime"
    SPEED = "speed"

    DATE = "date"
    TIME = "time"

    GEOMETRY = "geometry"
    BUS_STOP = "bus_stop"
    GROUPED_TERMINALS = "grouped_terminals"
    ENTRY_EXIT = "entry/exit"
    TRIP_ID = "trip_id"


class ProcessedGPSField(Enum):
    ID = "id"
    DEVICE_ID = "deviceid"
    LATITUDE = "latitude"
    LONGITUDE = "longitude"
    DEVICE_TIME = "devicetime"
    SPEED = "speed"

    DATE = "date"
    TIME = "time"

    GEOMETRY = "geometry"
    BUS_STOP = "bus_stop"
    GROUPED_TERMINALS = "grouped_terminals"
    ENTRY_EXIT = "entry/exit"
    TRIP_ID = "trip_id"


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


class TrajectoryField(Enum):
    ID = "id"
    DEVICE_ID = "deviceid"
    LATITUDE = "latitude"
    LONGITUDE = "longitude"
    DEVICE_TIME = "devicetime"
    SPEED = "speed"

    DATE = "date"
    TIME = "time"

    BUS_STOP = "bus_stop"
    TRIP_ID = "trip_id"

    DIRECTION = "direction"


class ExtractedStopField(Enum):
    ID = "id"
    DEVICE_ID = "deviceid"
    LATITUDE = "latitude"
    LONGITUDE = "longitude"
    DEVICE_TIME = "devicetime"
    SPEED = "speed"

    DATE = "date"
    TIME = "time"

    BUS_STOP = "bus_stop"
    TRIP_ID = "trip_id"

    DIRECTION = "direction"

    GROUPED_ENDS = "grouped_ends"


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
