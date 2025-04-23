from make87_messages_ros2.jazzy.trajectory_msgs.msg import joint_trajectory_pb2 as _joint_trajectory_pb2
from make87_messages_ros2.jazzy.trajectory_msgs.msg import multi_dof_joint_trajectory_pb2 as _multi_dof_joint_trajectory_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RobotTrajectory(_message.Message):
    __slots__ = ("joint_trajectory", "multi_dof_joint_trajectory")
    JOINT_TRAJECTORY_FIELD_NUMBER: _ClassVar[int]
    MULTI_DOF_JOINT_TRAJECTORY_FIELD_NUMBER: _ClassVar[int]
    joint_trajectory: _joint_trajectory_pb2.JointTrajectory
    multi_dof_joint_trajectory: _multi_dof_joint_trajectory_pb2.MultiDOFJointTrajectory
    def __init__(self, joint_trajectory: _Optional[_Union[_joint_trajectory_pb2.JointTrajectory, _Mapping]] = ..., multi_dof_joint_trajectory: _Optional[_Union[_multi_dof_joint_trajectory_pb2.MultiDOFJointTrajectory, _Mapping]] = ...) -> None: ...
