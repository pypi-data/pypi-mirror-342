from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.webots_ros2_msgs.msg import urdf_robot_pb2 as _urdf_robot_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SpawnUrdfRobotRequest(_message.Message):
    __slots__ = ("header", "robot")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROBOT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    robot: _urdf_robot_pb2.UrdfRobot
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., robot: _Optional[_Union[_urdf_robot_pb2.UrdfRobot, _Mapping]] = ...) -> None: ...

class SpawnUrdfRobotResponse(_message.Message):
    __slots__ = ("header", "success")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ...) -> None: ...
