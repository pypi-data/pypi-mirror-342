from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TrafficSignInfo(_message.Message):
    __slots__ = ("header", "status", "camera_used", "navigation_used", "speed_units", "speed_limit")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CAMERA_USED_FIELD_NUMBER: _ClassVar[int]
    NAVIGATION_USED_FIELD_NUMBER: _ClassVar[int]
    SPEED_UNITS_FIELD_NUMBER: _ClassVar[int]
    SPEED_LIMIT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    status: int
    camera_used: bool
    navigation_used: bool
    speed_units: int
    speed_limit: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., status: _Optional[int] = ..., camera_used: bool = ..., navigation_used: bool = ..., speed_units: _Optional[int] = ..., speed_limit: _Optional[float] = ...) -> None: ...
