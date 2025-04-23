from make87_messages_ros2.jazzy.novatel_gps_msgs.msg import novatel_message_header_pb2 as _novatel_message_header_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NovatelVelocity(_message.Message):
    __slots__ = ("header", "novatel_msg_header", "solution_status", "velocity_type", "latency", "age", "horizontal_speed", "track_ground", "vertical_speed")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NOVATEL_MSG_HEADER_FIELD_NUMBER: _ClassVar[int]
    SOLUTION_STATUS_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    LATENCY_FIELD_NUMBER: _ClassVar[int]
    AGE_FIELD_NUMBER: _ClassVar[int]
    HORIZONTAL_SPEED_FIELD_NUMBER: _ClassVar[int]
    TRACK_GROUND_FIELD_NUMBER: _ClassVar[int]
    VERTICAL_SPEED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    novatel_msg_header: _novatel_message_header_pb2.NovatelMessageHeader
    solution_status: str
    velocity_type: str
    latency: float
    age: float
    horizontal_speed: float
    track_ground: float
    vertical_speed: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., novatel_msg_header: _Optional[_Union[_novatel_message_header_pb2.NovatelMessageHeader, _Mapping]] = ..., solution_status: _Optional[str] = ..., velocity_type: _Optional[str] = ..., latency: _Optional[float] = ..., age: _Optional[float] = ..., horizontal_speed: _Optional[float] = ..., track_ground: _Optional[float] = ..., vertical_speed: _Optional[float] = ...) -> None: ...
