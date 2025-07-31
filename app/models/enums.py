from enum import Enum


class PowerStatus(Enum):
    STOPPED = 0
    RUNNING = 1


class UPSStatus(Enum):
    Online = 0
