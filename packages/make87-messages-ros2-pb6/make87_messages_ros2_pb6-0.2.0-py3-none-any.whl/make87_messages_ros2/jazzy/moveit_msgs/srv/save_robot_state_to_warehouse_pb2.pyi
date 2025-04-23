from make87_messages_ros2.jazzy.moveit_msgs.msg import robot_state_pb2 as _robot_state_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SaveRobotStateToWarehouseRequest(_message.Message):
    __slots__ = ("name", "robot", "state")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ROBOT_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    name: str
    robot: str
    state: _robot_state_pb2.RobotState
    def __init__(self, name: _Optional[str] = ..., robot: _Optional[str] = ..., state: _Optional[_Union[_robot_state_pb2.RobotState, _Mapping]] = ...) -> None: ...

class SaveRobotStateToWarehouseResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
