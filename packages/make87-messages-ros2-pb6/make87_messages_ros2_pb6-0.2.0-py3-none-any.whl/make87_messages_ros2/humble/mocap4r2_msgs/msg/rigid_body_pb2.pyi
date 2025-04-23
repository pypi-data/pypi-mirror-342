from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.humble.mocap4r2_msgs.msg import marker_pb2 as _marker_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RigidBody(_message.Message):
    __slots__ = ("header", "rigid_body_name", "markers", "pose")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    RIGID_BODY_NAME_FIELD_NUMBER: _ClassVar[int]
    MARKERS_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    rigid_body_name: str
    markers: _containers.RepeatedCompositeFieldContainer[_marker_pb2.Marker]
    pose: _pose_pb2.Pose
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., rigid_body_name: _Optional[str] = ..., markers: _Optional[_Iterable[_Union[_marker_pb2.Marker, _Mapping]]] = ..., pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ...) -> None: ...
