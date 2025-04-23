from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rmf_fleet_msgs.msg import mode_parameter_pb2 as _mode_parameter_pb2
from make87_messages_ros2.humble.rmf_fleet_msgs.msg import robot_mode_pb2 as _robot_mode_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ModeRequest(_message.Message):
    __slots__ = ("header", "fleet_name", "robot_name", "mode", "task_id", "parameters")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FLEET_NAME_FIELD_NUMBER: _ClassVar[int]
    ROBOT_NAME_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    fleet_name: str
    robot_name: str
    mode: _robot_mode_pb2.RobotMode
    task_id: str
    parameters: _containers.RepeatedCompositeFieldContainer[_mode_parameter_pb2.ModeParameter]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., fleet_name: _Optional[str] = ..., robot_name: _Optional[str] = ..., mode: _Optional[_Union[_robot_mode_pb2.RobotMode, _Mapping]] = ..., task_id: _Optional[str] = ..., parameters: _Optional[_Iterable[_Union[_mode_parameter_pb2.ModeParameter, _Mapping]]] = ...) -> None: ...
