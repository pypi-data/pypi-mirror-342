from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetModeRequest(_message.Message):
    __slots__ = ("header", "base_mode", "custom_mode")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BASE_MODE_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_MODE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    base_mode: int
    custom_mode: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., base_mode: _Optional[int] = ..., custom_mode: _Optional[str] = ...) -> None: ...

class SetModeResponse(_message.Message):
    __slots__ = ("header", "mode_sent")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MODE_SENT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    mode_sent: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., mode_sent: bool = ...) -> None: ...
