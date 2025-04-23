from make87_messages_ros2.jazzy.rmf_fleet_msgs.msg import robot_state_pb2 as _robot_state_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FleetState(_message.Message):
    __slots__ = ("name", "robots")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ROBOTS_FIELD_NUMBER: _ClassVar[int]
    name: str
    robots: _containers.RepeatedCompositeFieldContainer[_robot_state_pb2.RobotState]
    def __init__(self, name: _Optional[str] = ..., robots: _Optional[_Iterable[_Union[_robot_state_pb2.RobotState, _Mapping]]] = ...) -> None: ...
