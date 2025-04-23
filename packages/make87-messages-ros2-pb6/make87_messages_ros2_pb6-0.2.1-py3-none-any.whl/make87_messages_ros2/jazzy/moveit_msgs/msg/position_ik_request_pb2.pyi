from make87_messages_ros2.jazzy.builtin_interfaces.msg import duration_pb2 as _duration_pb2
from make87_messages_ros2.jazzy.geometry_msgs.msg import pose_stamped_pb2 as _pose_stamped_pb2
from make87_messages_ros2.jazzy.moveit_msgs.msg import constraints_pb2 as _constraints_pb2
from make87_messages_ros2.jazzy.moveit_msgs.msg import robot_state_pb2 as _robot_state_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PositionIKRequest(_message.Message):
    __slots__ = ("group_name", "robot_state", "constraints", "avoid_collisions", "ik_link_name", "pose_stamped", "ik_link_names", "pose_stamped_vector", "timeout")
    GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    ROBOT_STATE_FIELD_NUMBER: _ClassVar[int]
    CONSTRAINTS_FIELD_NUMBER: _ClassVar[int]
    AVOID_COLLISIONS_FIELD_NUMBER: _ClassVar[int]
    IK_LINK_NAME_FIELD_NUMBER: _ClassVar[int]
    POSE_STAMPED_FIELD_NUMBER: _ClassVar[int]
    IK_LINK_NAMES_FIELD_NUMBER: _ClassVar[int]
    POSE_STAMPED_VECTOR_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    group_name: str
    robot_state: _robot_state_pb2.RobotState
    constraints: _constraints_pb2.Constraints
    avoid_collisions: bool
    ik_link_name: str
    pose_stamped: _pose_stamped_pb2.PoseStamped
    ik_link_names: _containers.RepeatedScalarFieldContainer[str]
    pose_stamped_vector: _containers.RepeatedCompositeFieldContainer[_pose_stamped_pb2.PoseStamped]
    timeout: _duration_pb2.Duration
    def __init__(self, group_name: _Optional[str] = ..., robot_state: _Optional[_Union[_robot_state_pb2.RobotState, _Mapping]] = ..., constraints: _Optional[_Union[_constraints_pb2.Constraints, _Mapping]] = ..., avoid_collisions: bool = ..., ik_link_name: _Optional[str] = ..., pose_stamped: _Optional[_Union[_pose_stamped_pb2.PoseStamped, _Mapping]] = ..., ik_link_names: _Optional[_Iterable[str]] = ..., pose_stamped_vector: _Optional[_Iterable[_Union[_pose_stamped_pb2.PoseStamped, _Mapping]]] = ..., timeout: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...) -> None: ...
