from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.nav_msgs.msg import path_pb2 as _path_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IsPathValidRequest(_message.Message):
    __slots__ = ("header", "path")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    path: _path_pb2.Path
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., path: _Optional[_Union[_path_pb2.Path, _Mapping]] = ...) -> None: ...

class IsPathValidResponse(_message.Message):
    __slots__ = ("header", "is_valid", "invalid_pose_indices")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    IS_VALID_FIELD_NUMBER: _ClassVar[int]
    INVALID_POSE_INDICES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    is_valid: bool
    invalid_pose_indices: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., is_valid: bool = ..., invalid_pose_indices: _Optional[_Iterable[int]] = ...) -> None: ...
