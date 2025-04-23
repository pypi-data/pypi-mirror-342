from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IODirection(_message.Message):
    __slots__ = ("header", "pin_5", "pin_6", "pin_7", "pin_8")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PIN_5_FIELD_NUMBER: _ClassVar[int]
    PIN_6_FIELD_NUMBER: _ClassVar[int]
    PIN_7_FIELD_NUMBER: _ClassVar[int]
    PIN_8_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    pin_5: int
    pin_6: int
    pin_7: int
    pin_8: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., pin_5: _Optional[int] = ..., pin_6: _Optional[int] = ..., pin_7: _Optional[int] = ..., pin_8: _Optional[int] = ...) -> None: ...
