from make87_messages_ros2.jazzy.moveit_msgs.msg import collision_object_pb2 as _collision_object_pb2
from make87_messages_ros2.jazzy.octomap_msgs.msg import octomap_with_pose_pb2 as _octomap_with_pose_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PlanningSceneWorld(_message.Message):
    __slots__ = ("collision_objects", "octomap")
    COLLISION_OBJECTS_FIELD_NUMBER: _ClassVar[int]
    OCTOMAP_FIELD_NUMBER: _ClassVar[int]
    collision_objects: _containers.RepeatedCompositeFieldContainer[_collision_object_pb2.CollisionObject]
    octomap: _octomap_with_pose_pb2.OctomapWithPose
    def __init__(self, collision_objects: _Optional[_Iterable[_Union[_collision_object_pb2.CollisionObject, _Mapping]]] = ..., octomap: _Optional[_Union[_octomap_with_pose_pb2.OctomapWithPose, _Mapping]] = ...) -> None: ...
