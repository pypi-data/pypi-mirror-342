from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Velocity(_message.Message):
    __slots__ = ("header", "velocity", "variance")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_FIELD_NUMBER: _ClassVar[int]
    VARIANCE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    velocity: float
    variance: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., velocity: _Optional[float] = ..., variance: _Optional[float] = ...) -> None: ...
