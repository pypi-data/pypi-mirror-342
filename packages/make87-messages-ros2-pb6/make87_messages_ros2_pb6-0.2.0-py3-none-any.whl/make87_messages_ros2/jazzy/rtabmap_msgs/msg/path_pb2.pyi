from make87_messages_ros2.jazzy.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Path(_message.Message):
    __slots__ = ("header", "node_ids", "poses")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NODE_IDS_FIELD_NUMBER: _ClassVar[int]
    POSES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    node_ids: _containers.RepeatedScalarFieldContainer[int]
    poses: _containers.RepeatedCompositeFieldContainer[_pose_pb2.Pose]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., node_ids: _Optional[_Iterable[int]] = ..., poses: _Optional[_Iterable[_Union[_pose_pb2.Pose, _Mapping]]] = ...) -> None: ...
