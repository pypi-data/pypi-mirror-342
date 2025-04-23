from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TmcInfo(_message.Message):
    __slots__ = ("header", "ros2_header", "interface_name", "board_voltage", "status_flag", "status", "motor_num", "velocity", "position", "torque")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    INTERFACE_NAME_FIELD_NUMBER: _ClassVar[int]
    BOARD_VOLTAGE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FLAG_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MOTOR_NUM_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    TORQUE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    interface_name: str
    board_voltage: float
    status_flag: int
    status: str
    motor_num: int
    velocity: float
    position: int
    torque: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., interface_name: _Optional[str] = ..., board_voltage: _Optional[float] = ..., status_flag: _Optional[int] = ..., status: _Optional[str] = ..., motor_num: _Optional[int] = ..., velocity: _Optional[float] = ..., position: _Optional[int] = ..., torque: _Optional[int] = ...) -> None: ...
