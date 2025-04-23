from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.moveit_msgs.msg import move_it_error_codes_pb2 as _move_it_error_codes_pb2
from make87_messages_ros2.humble.moveit_msgs.msg import robot_state_pb2 as _robot_state_pb2
from make87_messages_ros2.humble.moveit_msgs.msg import robot_trajectory_pb2 as _robot_trajectory_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MotionPlanDetailedResponse(_message.Message):
    __slots__ = ("header", "trajectory_start", "group_name", "trajectory", "description", "processing_time", "error_code")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TRAJECTORY_START_FIELD_NUMBER: _ClassVar[int]
    GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    TRAJECTORY_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PROCESSING_TIME_FIELD_NUMBER: _ClassVar[int]
    ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    trajectory_start: _robot_state_pb2.RobotState
    group_name: str
    trajectory: _containers.RepeatedCompositeFieldContainer[_robot_trajectory_pb2.RobotTrajectory]
    description: _containers.RepeatedScalarFieldContainer[str]
    processing_time: _containers.RepeatedScalarFieldContainer[float]
    error_code: _move_it_error_codes_pb2.MoveItErrorCodes
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., trajectory_start: _Optional[_Union[_robot_state_pb2.RobotState, _Mapping]] = ..., group_name: _Optional[str] = ..., trajectory: _Optional[_Iterable[_Union[_robot_trajectory_pb2.RobotTrajectory, _Mapping]]] = ..., description: _Optional[_Iterable[str]] = ..., processing_time: _Optional[_Iterable[float]] = ..., error_code: _Optional[_Union[_move_it_error_codes_pb2.MoveItErrorCodes, _Mapping]] = ...) -> None: ...
