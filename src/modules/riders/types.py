from enum import Enum


class RiderStatus(str, Enum):
    busy = "busy"
    available = "available"
