"""
Types used for type checking the library. Client developers can use these if they like,
but they're mostly for our own sanity checks during development/testing.
"""

from typing import TYPE_CHECKING, NotRequired, TypedDict, Union

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any

    from pax25.applications import BaseApplication
    from pax25.interfaces.types import (
        DummyInterfaceConfig,
        FileInterfaceConfig,
        SerialInterfaceConfig,
        TCPInterfaceConfig,
    )


class EmptyDict(TypedDict):
    """
    Empty dictionary.
    """


class ParameterSettings(TypedDict):
    """
    Tunable parameters. You can probably leave these alone.
    """

    retries: int
    retry_interval: int


class MonitoringSettings(TypedDict):
    """
    Settings for monitoring.
    """

    max_frame_log_size: int | None
    max_stations_tracked: int | None


# The StationConfig object should always be JSON-serializable. This way we'll eventually
# be able to use JSON for configuration files.


# This means that all interface configs will ALSO need to be JSON-serializable.
class StationConfig(TypedDict):
    """
    Configuration for a station.
    """

    name: str
    interfaces: dict[
        str,
        Union[
            "FileInterfaceConfig",
            "DummyInterfaceConfig",
            "SerialInterfaceConfig",
            "TCPInterfaceConfig",
        ],
    ]
    monitoring: NotRequired[MonitoringSettings]
    parameters: NotRequired[ParameterSettings]


# Map for the station's application registry
ApplicationMap = dict[str, dict[str, "BaseApplication[Any]"]]
