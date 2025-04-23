from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.septentrio_gnss_driver.msg import block_header_pb2 as _block_header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GALAuthStatus(_message.Message):
    __slots__ = ("header", "ros2_header", "block_header", "osnma_status", "trusted_time_delta", "gal_active_mask", "gal_authentic_mask", "gps_active_mask", "gps_authentic_mask")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    BLOCK_HEADER_FIELD_NUMBER: _ClassVar[int]
    OSNMA_STATUS_FIELD_NUMBER: _ClassVar[int]
    TRUSTED_TIME_DELTA_FIELD_NUMBER: _ClassVar[int]
    GAL_ACTIVE_MASK_FIELD_NUMBER: _ClassVar[int]
    GAL_AUTHENTIC_MASK_FIELD_NUMBER: _ClassVar[int]
    GPS_ACTIVE_MASK_FIELD_NUMBER: _ClassVar[int]
    GPS_AUTHENTIC_MASK_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    block_header: _block_header_pb2.BlockHeader
    osnma_status: int
    trusted_time_delta: float
    gal_active_mask: int
    gal_authentic_mask: int
    gps_active_mask: int
    gps_authentic_mask: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., block_header: _Optional[_Union[_block_header_pb2.BlockHeader, _Mapping]] = ..., osnma_status: _Optional[int] = ..., trusted_time_delta: _Optional[float] = ..., gal_active_mask: _Optional[int] = ..., gal_authentic_mask: _Optional[int] = ..., gps_active_mask: _Optional[int] = ..., gps_authentic_mask: _Optional[int] = ...) -> None: ...
