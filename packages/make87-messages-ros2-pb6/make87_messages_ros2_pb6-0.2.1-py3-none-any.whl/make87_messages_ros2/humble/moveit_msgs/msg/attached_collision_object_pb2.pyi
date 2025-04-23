from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.moveit_msgs.msg import collision_object_pb2 as _collision_object_pb2
from make87_messages_ros2.humble.trajectory_msgs.msg import joint_trajectory_pb2 as _joint_trajectory_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AttachedCollisionObject(_message.Message):
    __slots__ = ("header", "link_name", "object", "touch_links", "detach_posture", "weight")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LINK_NAME_FIELD_NUMBER: _ClassVar[int]
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    TOUCH_LINKS_FIELD_NUMBER: _ClassVar[int]
    DETACH_POSTURE_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    link_name: str
    object: _collision_object_pb2.CollisionObject
    touch_links: _containers.RepeatedScalarFieldContainer[str]
    detach_posture: _joint_trajectory_pb2.JointTrajectory
    weight: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., link_name: _Optional[str] = ..., object: _Optional[_Union[_collision_object_pb2.CollisionObject, _Mapping]] = ..., touch_links: _Optional[_Iterable[str]] = ..., detach_posture: _Optional[_Union[_joint_trajectory_pb2.JointTrajectory, _Mapping]] = ..., weight: _Optional[float] = ...) -> None: ...
