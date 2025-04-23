from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.mavros_msgs.msg import file_entry_pb2 as _file_entry_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FileListRequest(_message.Message):
    __slots__ = ("header", "dir_path")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DIR_PATH_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    dir_path: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., dir_path: _Optional[str] = ...) -> None: ...

class FileListResponse(_message.Message):
    __slots__ = ("header", "list", "success", "r_errno")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LIST_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    R_ERRNO_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    list: _containers.RepeatedCompositeFieldContainer[_file_entry_pb2.FileEntry]
    success: bool
    r_errno: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., list: _Optional[_Iterable[_Union[_file_entry_pb2.FileEntry, _Mapping]]] = ..., success: bool = ..., r_errno: _Optional[int] = ...) -> None: ...
