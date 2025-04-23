from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Mouse(_message.Message):
    __slots__ = ("header", "ros2_header", "integrated_x", "integrated_y", "frame_id", "last_squal")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    INTEGRATED_X_FIELD_NUMBER: _ClassVar[int]
    INTEGRATED_Y_FIELD_NUMBER: _ClassVar[int]
    FRAME_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_SQUAL_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    integrated_x: float
    integrated_y: float
    frame_id: int
    last_squal: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., integrated_x: _Optional[float] = ..., integrated_y: _Optional[float] = ..., frame_id: _Optional[int] = ..., last_squal: _Optional[int] = ...) -> None: ...
