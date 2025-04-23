from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.clearpath_platform_msgs.msg import drive_feedback_pb2 as _drive_feedback_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Feedback(_message.Message):
    __slots__ = ("header", "ros2_header", "drivers", "commanded_mode", "actual_mode")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    DRIVERS_FIELD_NUMBER: _ClassVar[int]
    COMMANDED_MODE_FIELD_NUMBER: _ClassVar[int]
    ACTUAL_MODE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    drivers: _containers.RepeatedCompositeFieldContainer[_drive_feedback_pb2.DriveFeedback]
    commanded_mode: int
    actual_mode: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., drivers: _Optional[_Iterable[_Union[_drive_feedback_pb2.DriveFeedback, _Mapping]]] = ..., commanded_mode: _Optional[int] = ..., actual_mode: _Optional[int] = ...) -> None: ...
