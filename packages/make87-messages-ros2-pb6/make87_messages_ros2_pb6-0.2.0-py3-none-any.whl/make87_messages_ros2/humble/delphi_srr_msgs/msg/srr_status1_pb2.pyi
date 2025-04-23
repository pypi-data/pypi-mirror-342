from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SrrStatus1(_message.Message):
    __slots__ = ("header", "ros2_header", "can_tx_look_type", "can_tx_dsp_timestamp", "can_tx_yaw_rate_calc", "can_tx_vehicle_speed_calc", "can_tx_scan_index", "can_tx_curvature")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_LOOK_TYPE_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_DSP_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_YAW_RATE_CALC_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_VEHICLE_SPEED_CALC_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_SCAN_INDEX_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_CURVATURE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    can_tx_look_type: bool
    can_tx_dsp_timestamp: int
    can_tx_yaw_rate_calc: float
    can_tx_vehicle_speed_calc: float
    can_tx_scan_index: int
    can_tx_curvature: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., can_tx_look_type: bool = ..., can_tx_dsp_timestamp: _Optional[int] = ..., can_tx_yaw_rate_calc: _Optional[float] = ..., can_tx_vehicle_speed_calc: _Optional[float] = ..., can_tx_scan_index: _Optional[int] = ..., can_tx_curvature: _Optional[float] = ...) -> None: ...
