from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.sensor_msgs.msg import nav_sat_fix_pb2 as _nav_sat_fix_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AddStaticTransformGpsRequest(_message.Message):
    __slots__ = ("header", "frame_id", "child_frame_id", "gps_position", "azimuth", "elevation", "bank")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FRAME_ID_FIELD_NUMBER: _ClassVar[int]
    CHILD_FRAME_ID_FIELD_NUMBER: _ClassVar[int]
    GPS_POSITION_FIELD_NUMBER: _ClassVar[int]
    AZIMUTH_FIELD_NUMBER: _ClassVar[int]
    ELEVATION_FIELD_NUMBER: _ClassVar[int]
    BANK_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    frame_id: str
    child_frame_id: str
    gps_position: _nav_sat_fix_pb2.NavSatFix
    azimuth: float
    elevation: float
    bank: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., frame_id: _Optional[str] = ..., child_frame_id: _Optional[str] = ..., gps_position: _Optional[_Union[_nav_sat_fix_pb2.NavSatFix, _Mapping]] = ..., azimuth: _Optional[float] = ..., elevation: _Optional[float] = ..., bank: _Optional[float] = ...) -> None: ...

class AddStaticTransformGpsResponse(_message.Message):
    __slots__ = ("header", "success")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ...) -> None: ...
