from make87_messages_ros2.rolling.moveit_msgs.msg import robot_state_pb2 as _robot_state_pb2
from make87_messages_ros2.rolling.moveit_msgs.msg import robot_trajectory_pb2 as _robot_trajectory_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DisplayTrajectory(_message.Message):
    __slots__ = ("model_id", "trajectory", "trajectory_start")
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    TRAJECTORY_FIELD_NUMBER: _ClassVar[int]
    TRAJECTORY_START_FIELD_NUMBER: _ClassVar[int]
    model_id: str
    trajectory: _containers.RepeatedCompositeFieldContainer[_robot_trajectory_pb2.RobotTrajectory]
    trajectory_start: _robot_state_pb2.RobotState
    def __init__(self, model_id: _Optional[str] = ..., trajectory: _Optional[_Iterable[_Union[_robot_trajectory_pb2.RobotTrajectory, _Mapping]]] = ..., trajectory_start: _Optional[_Union[_robot_state_pb2.RobotState, _Mapping]] = ...) -> None: ...
