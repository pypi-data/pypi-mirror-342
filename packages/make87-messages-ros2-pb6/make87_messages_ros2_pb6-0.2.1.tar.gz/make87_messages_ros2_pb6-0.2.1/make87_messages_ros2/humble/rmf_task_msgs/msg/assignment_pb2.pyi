from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Assignment(_message.Message):
    __slots__ = ("header", "is_assigned", "fleet_name", "expected_robot_name")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    IS_ASSIGNED_FIELD_NUMBER: _ClassVar[int]
    FLEET_NAME_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_ROBOT_NAME_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    is_assigned: bool
    fleet_name: str
    expected_robot_name: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., is_assigned: bool = ..., fleet_name: _Optional[str] = ..., expected_robot_name: _Optional[str] = ...) -> None: ...
