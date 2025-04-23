from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SensorStateInformation(_message.Message):
    __slots__ = ("header", "ros2_header", "lgp_version", "sensor_state", "customer_version", "internal_version")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    LGP_VERSION_FIELD_NUMBER: _ClassVar[int]
    SENSOR_STATE_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_VERSION_FIELD_NUMBER: _ClassVar[int]
    INTERNAL_VERSION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    lgp_version: int
    sensor_state: int
    customer_version: int
    internal_version: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., lgp_version: _Optional[int] = ..., sensor_state: _Optional[int] = ..., customer_version: _Optional[int] = ..., internal_version: _Optional[_Iterable[int]] = ...) -> None: ...
