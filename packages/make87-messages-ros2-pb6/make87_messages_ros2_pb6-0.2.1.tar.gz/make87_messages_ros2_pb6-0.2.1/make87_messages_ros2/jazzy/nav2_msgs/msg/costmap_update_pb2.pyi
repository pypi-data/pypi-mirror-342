from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CostmapUpdate(_message.Message):
    __slots__ = ("header", "x", "y", "size_x", "size_y", "data")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    SIZE_X_FIELD_NUMBER: _ClassVar[int]
    SIZE_Y_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    x: int
    y: int
    size_x: int
    size_y: int
    data: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., x: _Optional[int] = ..., y: _Optional[int] = ..., size_x: _Optional[int] = ..., size_y: _Optional[int] = ..., data: _Optional[_Iterable[int]] = ...) -> None: ...
