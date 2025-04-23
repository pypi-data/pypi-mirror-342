from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.novatel_gps_msgs.msg import novatel_message_header_pb2 as _novatel_message_header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Inscov(_message.Message):
    __slots__ = ("header", "ros2_header", "novatel_msg_header", "week", "seconds", "position_covariance", "attitude_covariance", "velocity_covariance")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    NOVATEL_MSG_HEADER_FIELD_NUMBER: _ClassVar[int]
    WEEK_FIELD_NUMBER: _ClassVar[int]
    SECONDS_FIELD_NUMBER: _ClassVar[int]
    POSITION_COVARIANCE_FIELD_NUMBER: _ClassVar[int]
    ATTITUDE_COVARIANCE_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_COVARIANCE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    novatel_msg_header: _novatel_message_header_pb2.NovatelMessageHeader
    week: int
    seconds: float
    position_covariance: _containers.RepeatedScalarFieldContainer[float]
    attitude_covariance: _containers.RepeatedScalarFieldContainer[float]
    velocity_covariance: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., novatel_msg_header: _Optional[_Union[_novatel_message_header_pb2.NovatelMessageHeader, _Mapping]] = ..., week: _Optional[int] = ..., seconds: _Optional[float] = ..., position_covariance: _Optional[_Iterable[float]] = ..., attitude_covariance: _Optional[_Iterable[float]] = ..., velocity_covariance: _Optional[_Iterable[float]] = ...) -> None: ...
