from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from make87_messages_ros2.rolling.tuw_multi_robot_msgs.msg import robot_goals_pb2 as _robot_goals_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RobotGoalsArray(_message.Message):
    __slots__ = ("header", "robots")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROBOTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    robots: _containers.RepeatedCompositeFieldContainer[_robot_goals_pb2.RobotGoals]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., robots: _Optional[_Iterable[_Union[_robot_goals_pb2.RobotGoals, _Mapping]]] = ...) -> None: ...
