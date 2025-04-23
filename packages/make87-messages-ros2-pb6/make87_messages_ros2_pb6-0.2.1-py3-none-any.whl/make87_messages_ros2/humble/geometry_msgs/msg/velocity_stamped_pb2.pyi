from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import twist_pb2 as _twist_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VelocityStamped(_message.Message):
    __slots__ = ("header", "ros2_header", "body_frame_id", "reference_frame_id", "velocity")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    BODY_FRAME_ID_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_FRAME_ID_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    body_frame_id: str
    reference_frame_id: str
    velocity: _twist_pb2.Twist
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., body_frame_id: _Optional[str] = ..., reference_frame_id: _Optional[str] = ..., velocity: _Optional[_Union[_twist_pb2.Twist, _Mapping]] = ...) -> None: ...
