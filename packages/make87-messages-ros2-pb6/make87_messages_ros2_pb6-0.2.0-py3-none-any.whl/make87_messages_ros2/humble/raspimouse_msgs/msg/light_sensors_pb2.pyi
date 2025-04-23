from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LightSensors(_message.Message):
    __slots__ = ("header", "forward_r", "forward_l", "left", "right")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FORWARD_R_FIELD_NUMBER: _ClassVar[int]
    FORWARD_L_FIELD_NUMBER: _ClassVar[int]
    LEFT_FIELD_NUMBER: _ClassVar[int]
    RIGHT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    forward_r: int
    forward_l: int
    left: int
    right: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., forward_r: _Optional[int] = ..., forward_l: _Optional[int] = ..., left: _Optional[int] = ..., right: _Optional[int] = ...) -> None: ...
