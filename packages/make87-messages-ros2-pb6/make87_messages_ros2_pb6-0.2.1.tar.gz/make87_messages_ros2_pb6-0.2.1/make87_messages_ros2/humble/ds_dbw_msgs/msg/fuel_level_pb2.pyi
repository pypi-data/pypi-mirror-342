from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FuelLevel(_message.Message):
    __slots__ = ("header", "ros2_header", "fuel_level", "fuel_range", "odometer")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    FUEL_LEVEL_FIELD_NUMBER: _ClassVar[int]
    FUEL_RANGE_FIELD_NUMBER: _ClassVar[int]
    ODOMETER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    fuel_level: float
    fuel_range: float
    odometer: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., fuel_level: _Optional[float] = ..., fuel_range: _Optional[float] = ..., odometer: _Optional[float] = ...) -> None: ...
