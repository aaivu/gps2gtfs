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
