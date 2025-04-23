from make87_messages_ros2.jazzy.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.jazzy.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BoundingBox3D(_message.Message):
    __slots__ = ("position", "size")
    POSITION_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    position: _pose_pb2.Pose
    size: _vector3_pb2.Vector3
    def __init__(self, position: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., size: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ...) -> None: ...
