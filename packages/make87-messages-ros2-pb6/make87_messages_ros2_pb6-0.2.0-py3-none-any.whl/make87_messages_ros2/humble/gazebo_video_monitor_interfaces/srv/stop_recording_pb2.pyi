from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StopRecordingRequest(_message.Message):
    __slots__ = ("header", "discard", "filename")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DISCARD_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    discard: bool
    filename: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., discard: bool = ..., filename: _Optional[str] = ...) -> None: ...

class StopRecordingResponse(_message.Message):
    __slots__ = ("header", "path", "success")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    path: str
    success: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., path: _Optional[str] = ..., success: bool = ...) -> None: ...
