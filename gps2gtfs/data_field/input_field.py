from enum import Enum


class RawGPSField(Enum):
    ID = "id"
    DEVICE_ID = "deviceid"
    LATITUDE = "latitude"
    LONGITUDE = "longitude"
    DEVICE_TIME = "devicetime"
    SPEED = "speed"


class TerminalField(Enum):
    TERMINAL_ID = "terminal_id"


class StopField(Enum):
    STOP_ID = "stop_id"
    DIRECTION = "direction"
