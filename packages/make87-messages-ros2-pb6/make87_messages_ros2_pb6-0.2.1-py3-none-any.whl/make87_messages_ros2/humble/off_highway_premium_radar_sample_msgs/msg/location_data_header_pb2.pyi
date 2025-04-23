from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.off_highway_premium_radar_sample_msgs.msg import operation_mode_pb2 as _operation_mode_pb2
from make87_messages_ros2.humble.off_highway_premium_radar_sample_msgs.msg import time_pb2 as _time_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LocationDataHeader(_message.Message):
    __slots__ = ("header", "ros2_header", "start_measurement", "lgp_version", "block_counter", "operation_mode", "data_measured", "num_locations")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    START_MEASUREMENT_FIELD_NUMBER: _ClassVar[int]
    LGP_VERSION_FIELD_NUMBER: _ClassVar[int]
    BLOCK_COUNTER_FIELD_NUMBER: _ClassVar[int]
    OPERATION_MODE_FIELD_NUMBER: _ClassVar[int]
    DATA_MEASURED_FIELD_NUMBER: _ClassVar[int]
    NUM_LOCATIONS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    start_measurement: _time_pb2.Time
    lgp_version: int
    block_counter: int
    operation_mode: _operation_mode_pb2.OperationMode
    data_measured: bool
    num_locations: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., start_measurement: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., lgp_version: _Optional[int] = ..., block_counter: _Optional[int] = ..., operation_mode: _Optional[_Union[_operation_mode_pb2.OperationMode, _Mapping]] = ..., data_measured: bool = ..., num_locations: _Optional[int] = ...) -> None: ...
