from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MrrHeaderSensorPosition(_message.Message):
    __slots__ = ("header", "can_sensor_polarity", "can_sensor_lat_offset", "can_sensor_long_offset", "can_sensor_hangle_offset")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CAN_SENSOR_POLARITY_FIELD_NUMBER: _ClassVar[int]
    CAN_SENSOR_LAT_OFFSET_FIELD_NUMBER: _ClassVar[int]
    CAN_SENSOR_LONG_OFFSET_FIELD_NUMBER: _ClassVar[int]
    CAN_SENSOR_HANGLE_OFFSET_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    can_sensor_polarity: bool
    can_sensor_lat_offset: float
    can_sensor_long_offset: float
    can_sensor_hangle_offset: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., can_sensor_polarity: bool = ..., can_sensor_lat_offset: _Optional[float] = ..., can_sensor_long_offset: _Optional[float] = ..., can_sensor_hangle_offset: _Optional[float] = ...) -> None: ...
