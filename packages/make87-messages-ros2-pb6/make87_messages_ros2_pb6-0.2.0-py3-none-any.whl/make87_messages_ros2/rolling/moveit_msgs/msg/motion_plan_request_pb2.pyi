from make87_messages_ros2.rolling.moveit_msgs.msg import constraints_pb2 as _constraints_pb2
from make87_messages_ros2.rolling.moveit_msgs.msg import generic_trajectory_pb2 as _generic_trajectory_pb2
from make87_messages_ros2.rolling.moveit_msgs.msg import robot_state_pb2 as _robot_state_pb2
from make87_messages_ros2.rolling.moveit_msgs.msg import trajectory_constraints_pb2 as _trajectory_constraints_pb2
from make87_messages_ros2.rolling.moveit_msgs.msg import workspace_parameters_pb2 as _workspace_parameters_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MotionPlanRequest(_message.Message):
    __slots__ = ("workspace_parameters", "start_state", "goal_constraints", "path_constraints", "trajectory_constraints", "reference_trajectories", "pipeline_id", "planner_id", "group_name", "num_planning_attempts", "allowed_planning_time", "max_velocity_scaling_factor", "max_acceleration_scaling_factor", "cartesian_speed_limited_link", "max_cartesian_speed")
    WORKSPACE_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    START_STATE_FIELD_NUMBER: _ClassVar[int]
    GOAL_CONSTRAINTS_FIELD_NUMBER: _ClassVar[int]
    PATH_CONSTRAINTS_FIELD_NUMBER: _ClassVar[int]
    TRAJECTORY_CONSTRAINTS_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_TRAJECTORIES_FIELD_NUMBER: _ClassVar[int]
    PIPELINE_ID_FIELD_NUMBER: _ClassVar[int]
    PLANNER_ID_FIELD_NUMBER: _ClassVar[int]
    GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    NUM_PLANNING_ATTEMPTS_FIELD_NUMBER: _ClassVar[int]
    ALLOWED_PLANNING_TIME_FIELD_NUMBER: _ClassVar[int]
    MAX_VELOCITY_SCALING_FACTOR_FIELD_NUMBER: _ClassVar[int]
    MAX_ACCELERATION_SCALING_FACTOR_FIELD_NUMBER: _ClassVar[int]
    CARTESIAN_SPEED_LIMITED_LINK_FIELD_NUMBER: _ClassVar[int]
    MAX_CARTESIAN_SPEED_FIELD_NUMBER: _ClassVar[int]
    workspace_parameters: _workspace_parameters_pb2.WorkspaceParameters
    start_state: _robot_state_pb2.RobotState
    goal_constraints: _containers.RepeatedCompositeFieldContainer[_constraints_pb2.Constraints]
    path_constraints: _constraints_pb2.Constraints
    trajectory_constraints: _trajectory_constraints_pb2.TrajectoryConstraints
    reference_trajectories: _containers.RepeatedCompositeFieldContainer[_generic_trajectory_pb2.GenericTrajectory]
    pipeline_id: str
    planner_id: str
    group_name: str
    num_planning_attempts: int
    allowed_planning_time: float
    max_velocity_scaling_factor: float
    max_acceleration_scaling_factor: float
    cartesian_speed_limited_link: str
    max_cartesian_speed: float
    def __init__(self, workspace_parameters: _Optional[_Union[_workspace_parameters_pb2.WorkspaceParameters, _Mapping]] = ..., start_state: _Optional[_Union[_robot_state_pb2.RobotState, _Mapping]] = ..., goal_constraints: _Optional[_Iterable[_Union[_constraints_pb2.Constraints, _Mapping]]] = ..., path_constraints: _Optional[_Union[_constraints_pb2.Constraints, _Mapping]] = ..., trajectory_constraints: _Optional[_Union[_trajectory_constraints_pb2.TrajectoryConstraints, _Mapping]] = ..., reference_trajectories: _Optional[_Iterable[_Union[_generic_trajectory_pb2.GenericTrajectory, _Mapping]]] = ..., pipeline_id: _Optional[str] = ..., planner_id: _Optional[str] = ..., group_name: _Optional[str] = ..., num_planning_attempts: _Optional[int] = ..., allowed_planning_time: _Optional[float] = ..., max_velocity_scaling_factor: _Optional[float] = ..., max_acceleration_scaling_factor: _Optional[float] = ..., cartesian_speed_limited_link: _Optional[str] = ..., max_cartesian_speed: _Optional[float] = ...) -> None: ...
