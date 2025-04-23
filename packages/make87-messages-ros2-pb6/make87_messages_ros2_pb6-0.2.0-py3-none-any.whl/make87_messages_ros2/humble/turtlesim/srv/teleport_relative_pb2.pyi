from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TeleportRelativeRequest(_message.Message):
    __slots__ = ("header", "linear", "angular")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LINEAR_FIELD_NUMBER: _ClassVar[int]
    ANGULAR_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    linear: float
    angular: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., linear: _Optional[float] = ..., angular: _Optional[float] = ...) -> None: ...

class TeleportRelativeResponse(_message.Message):
    __slots__ = ("header",)
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...
