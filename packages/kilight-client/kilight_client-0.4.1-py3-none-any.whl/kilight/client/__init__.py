"""kilight.client package for interfacing with KiLight open hardware light controllers."""

__version__ = "0.4.1"

__all__ = [
    "DEFAULT_PORT",
    "MIN_COLOR_TEMP",
    "MAX_COLOR_TEMP",
    "Connector",
    "Device",
    "OutputIdentifier",
    "OutputState",
    "DeviceState",
    "OutputIdUtil"
]

from kilight.protocol import OutputIdentifier

from .const import DEFAULT_PORT, MIN_COLOR_TEMP, MAX_COLOR_TEMP
from .connector import Connector
from .device import Device
from .models import OutputState, DeviceState
from .util import OutputIdUtil