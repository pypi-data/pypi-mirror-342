from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class FileReadRequest(_message.Message):
    __slots__ = ("file_path", "offset", "size")
    FILE_PATH_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    file_path: str
    offset: int
    size: int
    def __init__(self, file_path: _Optional[str] = ..., offset: _Optional[int] = ..., size: _Optional[int] = ...) -> None: ...

class FileReadResponse(_message.Message):
    __slots__ = ("data", "success", "r_errno")
    DATA_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    R_ERRNO_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedScalarFieldContainer[int]
    success: bool
    r_errno: int
    def __init__(self, data: _Optional[_Iterable[int]] = ..., success: bool = ..., r_errno: _Optional[int] = ...) -> None: ...
