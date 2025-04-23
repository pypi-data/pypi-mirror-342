from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SaveGeometryToFileRequest(_message.Message):
    __slots__ = ("header", "file_path_and_name")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FILE_PATH_AND_NAME_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    file_path_and_name: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., file_path_and_name: _Optional[str] = ...) -> None: ...

class SaveGeometryToFileResponse(_message.Message):
    __slots__ = ("header", "success")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ...) -> None: ...
