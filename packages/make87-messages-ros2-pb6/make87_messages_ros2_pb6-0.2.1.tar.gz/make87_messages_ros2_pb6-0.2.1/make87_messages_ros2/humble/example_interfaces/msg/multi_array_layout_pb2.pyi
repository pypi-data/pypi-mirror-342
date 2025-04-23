from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.example_interfaces.msg import multi_array_dimension_pb2 as _multi_array_dimension_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MultiArrayLayout(_message.Message):
    __slots__ = ("header", "dim", "data_offset")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DIM_FIELD_NUMBER: _ClassVar[int]
    DATA_OFFSET_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    dim: _containers.RepeatedCompositeFieldContainer[_multi_array_dimension_pb2.MultiArrayDimension]
    data_offset: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., dim: _Optional[_Iterable[_Union[_multi_array_dimension_pb2.MultiArrayDimension, _Mapping]]] = ..., data_offset: _Optional[int] = ...) -> None: ...
