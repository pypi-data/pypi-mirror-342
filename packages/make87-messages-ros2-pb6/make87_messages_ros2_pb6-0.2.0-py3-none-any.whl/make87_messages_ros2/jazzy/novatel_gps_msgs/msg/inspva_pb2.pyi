from make87_messages_ros2.jazzy.novatel_gps_msgs.msg import novatel_message_header_pb2 as _novatel_message_header_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Inspva(_message.Message):
    __slots__ = ("header", "novatel_msg_header", "week", "seconds", "latitude", "longitude", "height", "north_velocity", "east_velocity", "up_velocity", "roll", "pitch", "azimuth", "status")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NOVATEL_MSG_HEADER_FIELD_NUMBER: _ClassVar[int]
    WEEK_FIELD_NUMBER: _ClassVar[int]
    SECONDS_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    NORTH_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    EAST_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    UP_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    ROLL_FIELD_NUMBER: _ClassVar[int]
    PITCH_FIELD_NUMBER: _ClassVar[int]
    AZIMUTH_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    novatel_msg_header: _novatel_message_header_pb2.NovatelMessageHeader
    week: int
    seconds: float
    latitude: float
    longitude: float
    height: float
    north_velocity: float
    east_velocity: float
    up_velocity: float
    roll: float
    pitch: float
    azimuth: float
    status: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., novatel_msg_header: _Optional[_Union[_novatel_message_header_pb2.NovatelMessageHeader, _Mapping]] = ..., week: _Optional[int] = ..., seconds: _Optional[float] = ..., latitude: _Optional[float] = ..., longitude: _Optional[float] = ..., height: _Optional[float] = ..., north_velocity: _Optional[float] = ..., east_velocity: _Optional[float] = ..., up_velocity: _Optional[float] = ..., roll: _Optional[float] = ..., pitch: _Optional[float] = ..., azimuth: _Optional[float] = ..., status: _Optional[str] = ...) -> None: ...
