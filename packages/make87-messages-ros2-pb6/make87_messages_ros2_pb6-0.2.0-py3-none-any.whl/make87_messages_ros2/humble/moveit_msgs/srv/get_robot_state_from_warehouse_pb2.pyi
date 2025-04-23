from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.moveit_msgs.msg import robot_state_pb2 as _robot_state_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetRobotStateFromWarehouseRequest(_message.Message):
    __slots__ = ("header", "name", "robot")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ROBOT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    name: str
    robot: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., name: _Optional[str] = ..., robot: _Optional[str] = ...) -> None: ...

class GetRobotStateFromWarehouseResponse(_message.Message):
    __slots__ = ("header", "state")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    state: _robot_state_pb2.RobotState
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., state: _Optional[_Union[_robot_state_pb2.RobotState, _Mapping]] = ...) -> None: ...
