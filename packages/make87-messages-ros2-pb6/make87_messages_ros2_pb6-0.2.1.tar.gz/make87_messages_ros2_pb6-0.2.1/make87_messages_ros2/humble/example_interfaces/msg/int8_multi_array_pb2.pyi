from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.example_interfaces.msg import multi_array_layout_pb2 as _multi_array_layout_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Int8MultiArray(_message.Message):
    __slots__ = ("header", "layout", "data")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LAYOUT_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    layout: _multi_array_layout_pb2.MultiArrayLayout
    data: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., layout: _Optional[_Union[_multi_array_layout_pb2.MultiArrayLayout, _Mapping]] = ..., data: _Optional[_Iterable[int]] = ...) -> None: ...
