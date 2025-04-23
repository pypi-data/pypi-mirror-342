from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ChargingAssignment(_message.Message):
    __slots__ = ("header", "robot_name", "waypoint_name", "mode")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROBOT_NAME_FIELD_NUMBER: _ClassVar[int]
    WAYPOINT_NAME_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    robot_name: str
    waypoint_name: str
    mode: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., robot_name: _Optional[str] = ..., waypoint_name: _Optional[str] = ..., mode: _Optional[int] = ...) -> None: ...
