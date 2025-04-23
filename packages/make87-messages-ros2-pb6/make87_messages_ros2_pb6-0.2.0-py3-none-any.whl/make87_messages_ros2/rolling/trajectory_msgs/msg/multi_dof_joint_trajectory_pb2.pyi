from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from make87_messages_ros2.rolling.trajectory_msgs.msg import multi_dof_joint_trajectory_point_pb2 as _multi_dof_joint_trajectory_point_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MultiDOFJointTrajectory(_message.Message):
    __slots__ = ("header", "joint_names", "points")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    JOINT_NAMES_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    joint_names: _containers.RepeatedScalarFieldContainer[str]
    points: _containers.RepeatedCompositeFieldContainer[_multi_dof_joint_trajectory_point_pb2.MultiDOFJointTrajectoryPoint]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., joint_names: _Optional[_Iterable[str]] = ..., points: _Optional[_Iterable[_Union[_multi_dof_joint_trajectory_point_pb2.MultiDOFJointTrajectoryPoint, _Mapping]]] = ...) -> None: ...
