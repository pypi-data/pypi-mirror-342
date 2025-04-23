from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rtabmap_msgs.msg import node_pb2 as _node_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetNodeDataRequest(_message.Message):
    __slots__ = ("header", "ids", "images", "scan", "grid", "user_data")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    IDS_FIELD_NUMBER: _ClassVar[int]
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    SCAN_FIELD_NUMBER: _ClassVar[int]
    GRID_FIELD_NUMBER: _ClassVar[int]
    USER_DATA_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ids: _containers.RepeatedScalarFieldContainer[int]
    images: bool
    scan: bool
    grid: bool
    user_data: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ids: _Optional[_Iterable[int]] = ..., images: bool = ..., scan: bool = ..., grid: bool = ..., user_data: bool = ...) -> None: ...

class GetNodeDataResponse(_message.Message):
    __slots__ = ("header", "data")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    data: _containers.RepeatedCompositeFieldContainer[_node_pb2.Node]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., data: _Optional[_Iterable[_Union[_node_pb2.Node, _Mapping]]] = ...) -> None: ...
