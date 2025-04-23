from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MountControl(_message.Message):
    __slots__ = ("header", "mode", "pitch", "roll", "yaw", "altitude", "latitude", "longitude")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    PITCH_FIELD_NUMBER: _ClassVar[int]
    ROLL_FIELD_NUMBER: _ClassVar[int]
    YAW_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    mode: int
    pitch: float
    roll: float
    yaw: float
    altitude: float
    latitude: float
    longitude: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., mode: _Optional[int] = ..., pitch: _Optional[float] = ..., roll: _Optional[float] = ..., yaw: _Optional[float] = ..., altitude: _Optional[float] = ..., latitude: _Optional[float] = ..., longitude: _Optional[float] = ...) -> None: ...
