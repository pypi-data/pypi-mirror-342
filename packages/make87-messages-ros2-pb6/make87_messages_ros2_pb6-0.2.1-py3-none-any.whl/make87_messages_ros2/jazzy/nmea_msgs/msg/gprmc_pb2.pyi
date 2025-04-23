from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Gprmc(_message.Message):
    __slots__ = ("header", "message_id", "utc_seconds", "position_status", "lat", "lon", "lat_dir", "lon_dir", "speed", "track", "date", "mag_var", "mag_var_direction", "mode_indicator")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    UTC_SECONDS_FIELD_NUMBER: _ClassVar[int]
    POSITION_STATUS_FIELD_NUMBER: _ClassVar[int]
    LAT_FIELD_NUMBER: _ClassVar[int]
    LON_FIELD_NUMBER: _ClassVar[int]
    LAT_DIR_FIELD_NUMBER: _ClassVar[int]
    LON_DIR_FIELD_NUMBER: _ClassVar[int]
    SPEED_FIELD_NUMBER: _ClassVar[int]
    TRACK_FIELD_NUMBER: _ClassVar[int]
    DATE_FIELD_NUMBER: _ClassVar[int]
    MAG_VAR_FIELD_NUMBER: _ClassVar[int]
    MAG_VAR_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    MODE_INDICATOR_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    message_id: str
    utc_seconds: float
    position_status: str
    lat: float
    lon: float
    lat_dir: str
    lon_dir: str
    speed: float
    track: float
    date: str
    mag_var: float
    mag_var_direction: str
    mode_indicator: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., message_id: _Optional[str] = ..., utc_seconds: _Optional[float] = ..., position_status: _Optional[str] = ..., lat: _Optional[float] = ..., lon: _Optional[float] = ..., lat_dir: _Optional[str] = ..., lon_dir: _Optional[str] = ..., speed: _Optional[float] = ..., track: _Optional[float] = ..., date: _Optional[str] = ..., mag_var: _Optional[float] = ..., mag_var_direction: _Optional[str] = ..., mode_indicator: _Optional[str] = ...) -> None: ...
