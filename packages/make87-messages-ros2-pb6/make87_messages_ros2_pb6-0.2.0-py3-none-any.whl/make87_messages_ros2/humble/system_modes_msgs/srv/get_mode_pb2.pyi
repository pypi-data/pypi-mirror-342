from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetModeRequest(_message.Message):
    __slots__ = ("header",)
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...

class GetModeResponse(_message.Message):
    __slots__ = ("header", "current_mode")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CURRENT_MODE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    current_mode: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., current_mode: _Optional[str] = ...) -> None: ...
