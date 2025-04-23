from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BodyRequestRequest(_message.Message):
    __slots__ = ("header", "body_name")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BODY_NAME_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    body_name: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., body_name: _Optional[str] = ...) -> None: ...

class BodyRequestResponse(_message.Message):
    __slots__ = ("header",)
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...
