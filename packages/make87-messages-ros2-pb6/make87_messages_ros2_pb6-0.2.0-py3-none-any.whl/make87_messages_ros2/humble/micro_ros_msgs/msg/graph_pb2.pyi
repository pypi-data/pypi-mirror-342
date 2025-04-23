from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.micro_ros_msgs.msg import node_pb2 as _node_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Graph(_message.Message):
    __slots__ = ("header", "nodes")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NODES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    nodes: _containers.RepeatedCompositeFieldContainer[_node_pb2.Node]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., nodes: _Optional[_Iterable[_Union[_node_pb2.Node, _Mapping]]] = ...) -> None: ...
