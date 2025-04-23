from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.as2_msgs.msg import control_mode_pb2 as _control_mode_pb2
from make87_messages_ros2.humble.as2_msgs.msg import platform_status_pb2 as _platform_status_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PlatformInfo(_message.Message):
    __slots__ = ("header", "ros2_header", "connected", "armed", "offboard", "status", "current_control_mode")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    CONNECTED_FIELD_NUMBER: _ClassVar[int]
    ARMED_FIELD_NUMBER: _ClassVar[int]
    OFFBOARD_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CURRENT_CONTROL_MODE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    connected: bool
    armed: bool
    offboard: bool
    status: _platform_status_pb2.PlatformStatus
    current_control_mode: _control_mode_pb2.ControlMode
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., connected: bool = ..., armed: bool = ..., offboard: bool = ..., status: _Optional[_Union[_platform_status_pb2.PlatformStatus, _Mapping]] = ..., current_control_mode: _Optional[_Union[_control_mode_pb2.ControlMode, _Mapping]] = ...) -> None: ...
