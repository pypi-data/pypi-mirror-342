from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RelocalizeFromGNSSRequest(_message.Message):
    __slots__ = ("header",)
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...

class RelocalizeFromGNSSResponse(_message.Message):
    __slots__ = ("header", "accepted")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ACCEPTED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    accepted: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., accepted: bool = ...) -> None: ...
