from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BasicSrvRequest(_message.Message):
    __slots__ = ("header", "req")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    REQ_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    req: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., req: _Optional[str] = ...) -> None: ...

class BasicSrvResponse(_message.Message):
    __slots__ = ("header", "resp")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    RESP_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    resp: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., resp: _Optional[str] = ...) -> None: ...
