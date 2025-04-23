from make87_messages_ros2.rolling.moveit_msgs.msg import joint_limits_pb2 as _joint_limits_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class KinematicSolverInfo(_message.Message):
    __slots__ = ("joint_names", "limits", "link_names")
    JOINT_NAMES_FIELD_NUMBER: _ClassVar[int]
    LIMITS_FIELD_NUMBER: _ClassVar[int]
    LINK_NAMES_FIELD_NUMBER: _ClassVar[int]
    joint_names: _containers.RepeatedScalarFieldContainer[str]
    limits: _containers.RepeatedCompositeFieldContainer[_joint_limits_pb2.JointLimits]
    link_names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, joint_names: _Optional[_Iterable[str]] = ..., limits: _Optional[_Iterable[_Union[_joint_limits_pb2.JointLimits, _Mapping]]] = ..., link_names: _Optional[_Iterable[str]] = ...) -> None: ...
