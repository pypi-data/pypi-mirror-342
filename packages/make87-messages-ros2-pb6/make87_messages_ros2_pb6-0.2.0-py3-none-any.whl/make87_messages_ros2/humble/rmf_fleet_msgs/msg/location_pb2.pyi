from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Location(_message.Message):
    __slots__ = ("header", "t", "x", "y", "yaw", "obey_approach_speed_limit", "approach_speed_limit", "level_name", "index")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    T_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    YAW_FIELD_NUMBER: _ClassVar[int]
    OBEY_APPROACH_SPEED_LIMIT_FIELD_NUMBER: _ClassVar[int]
    APPROACH_SPEED_LIMIT_FIELD_NUMBER: _ClassVar[int]
    LEVEL_NAME_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    t: _time_pb2.Time
    x: float
    y: float
    yaw: float
    obey_approach_speed_limit: bool
    approach_speed_limit: float
    level_name: str
    index: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., t: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., x: _Optional[float] = ..., y: _Optional[float] = ..., yaw: _Optional[float] = ..., obey_approach_speed_limit: bool = ..., approach_speed_limit: _Optional[float] = ..., level_name: _Optional[str] = ..., index: _Optional[int] = ...) -> None: ...
