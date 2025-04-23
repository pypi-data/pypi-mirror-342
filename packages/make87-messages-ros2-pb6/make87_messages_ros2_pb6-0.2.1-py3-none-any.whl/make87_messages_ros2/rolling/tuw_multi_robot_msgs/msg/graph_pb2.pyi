from make87_messages_ros2.rolling.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from make87_messages_ros2.rolling.tuw_multi_robot_msgs.msg import vertex_pb2 as _vertex_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Graph(_message.Message):
    __slots__ = ("header", "origin", "vertices")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    VERTICES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    origin: _pose_pb2.Pose
    vertices: _containers.RepeatedCompositeFieldContainer[_vertex_pb2.Vertex]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., origin: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., vertices: _Optional[_Iterable[_Union[_vertex_pb2.Vertex, _Mapping]]] = ...) -> None: ...
