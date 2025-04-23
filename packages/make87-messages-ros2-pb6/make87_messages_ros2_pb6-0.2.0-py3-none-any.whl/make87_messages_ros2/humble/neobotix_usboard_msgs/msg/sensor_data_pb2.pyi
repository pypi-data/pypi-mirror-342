from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SensorData(_message.Message):
    __slots__ = ("header", "distance", "warn", "alarm", "active")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_FIELD_NUMBER: _ClassVar[int]
    WARN_FIELD_NUMBER: _ClassVar[int]
    ALARM_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    distance: int
    warn: bool
    alarm: bool
    active: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., distance: _Optional[int] = ..., warn: bool = ..., alarm: bool = ..., active: bool = ...) -> None: ...
