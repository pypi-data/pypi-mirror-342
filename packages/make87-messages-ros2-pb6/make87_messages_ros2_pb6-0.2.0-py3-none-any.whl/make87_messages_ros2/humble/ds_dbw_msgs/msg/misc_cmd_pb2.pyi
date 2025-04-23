from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.ds_dbw_msgs.msg import prk_brk_cmd_pb2 as _prk_brk_cmd_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MiscCmd(_message.Message):
    __slots__ = ("header", "ros2_header", "parking_brake")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    PARKING_BRAKE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    parking_brake: _prk_brk_cmd_pb2.PrkBrkCmd
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., parking_brake: _Optional[_Union[_prk_brk_cmd_pb2.PrkBrkCmd, _Mapping]] = ...) -> None: ...
