from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FileChecksumRequest(_message.Message):
    __slots__ = ("header", "file_path")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FILE_PATH_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    file_path: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., file_path: _Optional[str] = ...) -> None: ...

class FileChecksumResponse(_message.Message):
    __slots__ = ("header", "crc32", "success", "r_errno")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CRC32_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    R_ERRNO_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    crc32: int
    success: bool
    r_errno: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., crc32: _Optional[int] = ..., success: bool = ..., r_errno: _Optional[int] = ...) -> None: ...
