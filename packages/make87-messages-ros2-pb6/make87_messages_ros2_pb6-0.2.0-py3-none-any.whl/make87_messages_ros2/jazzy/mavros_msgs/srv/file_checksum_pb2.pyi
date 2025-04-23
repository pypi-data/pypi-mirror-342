from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class FileChecksumRequest(_message.Message):
    __slots__ = ("file_path",)
    FILE_PATH_FIELD_NUMBER: _ClassVar[int]
    file_path: str
    def __init__(self, file_path: _Optional[str] = ...) -> None: ...

class FileChecksumResponse(_message.Message):
    __slots__ = ("crc32", "success", "r_errno")
    CRC32_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    R_ERRNO_FIELD_NUMBER: _ClassVar[int]
    crc32: int
    success: bool
    r_errno: int
    def __init__(self, crc32: _Optional[int] = ..., success: bool = ..., r_errno: _Optional[int] = ...) -> None: ...
