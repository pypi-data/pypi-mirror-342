from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RecStat(_message.Message):
    __slots__ = ("header", "leap_sec", "clk_reset")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LEAP_SEC_FIELD_NUMBER: _ClassVar[int]
    CLK_RESET_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    leap_sec: bool
    clk_reset: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., leap_sec: bool = ..., clk_reset: bool = ...) -> None: ...
