from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FileOpenRequest(_message.Message):
    __slots__ = ("header", "file_path", "mode")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FILE_PATH_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    file_path: str
    mode: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., file_path: _Optional[str] = ..., mode: _Optional[int] = ...) -> None: ...

class FileOpenResponse(_message.Message):
    __slots__ = ("header", "size", "success", "r_errno")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    R_ERRNO_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    size: int
    success: bool
    r_errno: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., size: _Optional[int] = ..., success: bool = ..., r_errno: _Optional[int] = ...) -> None: ...
