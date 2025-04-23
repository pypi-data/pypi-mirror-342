from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OpticalFlowRad(_message.Message):
    __slots__ = ("header", "integration_time_us", "integrated_x", "integrated_y", "integrated_xgyro", "integrated_ygyro", "integrated_zgyro", "temperature", "quality", "time_delta_distance_us", "distance")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    INTEGRATION_TIME_US_FIELD_NUMBER: _ClassVar[int]
    INTEGRATED_X_FIELD_NUMBER: _ClassVar[int]
    INTEGRATED_Y_FIELD_NUMBER: _ClassVar[int]
    INTEGRATED_XGYRO_FIELD_NUMBER: _ClassVar[int]
    INTEGRATED_YGYRO_FIELD_NUMBER: _ClassVar[int]
    INTEGRATED_ZGYRO_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    QUALITY_FIELD_NUMBER: _ClassVar[int]
    TIME_DELTA_DISTANCE_US_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    integration_time_us: int
    integrated_x: float
    integrated_y: float
    integrated_xgyro: float
    integrated_ygyro: float
    integrated_zgyro: float
    temperature: int
    quality: int
    time_delta_distance_us: int
    distance: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., integration_time_us: _Optional[int] = ..., integrated_x: _Optional[float] = ..., integrated_y: _Optional[float] = ..., integrated_xgyro: _Optional[float] = ..., integrated_ygyro: _Optional[float] = ..., integrated_zgyro: _Optional[float] = ..., temperature: _Optional[int] = ..., quality: _Optional[int] = ..., time_delta_distance_us: _Optional[int] = ..., distance: _Optional[float] = ...) -> None: ...
