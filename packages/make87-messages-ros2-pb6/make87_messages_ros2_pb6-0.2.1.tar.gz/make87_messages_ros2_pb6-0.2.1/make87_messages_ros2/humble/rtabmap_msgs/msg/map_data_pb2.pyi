from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rtabmap_msgs.msg import map_graph_pb2 as _map_graph_pb2
from make87_messages_ros2.humble.rtabmap_msgs.msg import node_pb2 as _node_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MapData(_message.Message):
    __slots__ = ("header", "ros2_header", "graph", "nodes")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    GRAPH_FIELD_NUMBER: _ClassVar[int]
    NODES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    graph: _map_graph_pb2.MapGraph
    nodes: _containers.RepeatedCompositeFieldContainer[_node_pb2.Node]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., graph: _Optional[_Union[_map_graph_pb2.MapGraph, _Mapping]] = ..., nodes: _Optional[_Iterable[_Union[_node_pb2.Node, _Mapping]]] = ...) -> None: ...
