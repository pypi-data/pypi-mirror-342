from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EsrVehicle5(_message.Message):
    __slots__ = ("header", "ros2_header", "oversteer_understeer", "yaw_rate_bias_shift", "beamwidth_vert", "funnel_offset_left", "funnel_offset_right", "cw_blockage_threshold", "distance_rear_axle", "wheelbase", "steering_gear_ratio")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    OVERSTEER_UNDERSTEER_FIELD_NUMBER: _ClassVar[int]
    YAW_RATE_BIAS_SHIFT_FIELD_NUMBER: _ClassVar[int]
    BEAMWIDTH_VERT_FIELD_NUMBER: _ClassVar[int]
    FUNNEL_OFFSET_LEFT_FIELD_NUMBER: _ClassVar[int]
    FUNNEL_OFFSET_RIGHT_FIELD_NUMBER: _ClassVar[int]
    CW_BLOCKAGE_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_REAR_AXLE_FIELD_NUMBER: _ClassVar[int]
    WHEELBASE_FIELD_NUMBER: _ClassVar[int]
    STEERING_GEAR_RATIO_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    oversteer_understeer: int
    yaw_rate_bias_shift: bool
    beamwidth_vert: float
    funnel_offset_left: float
    funnel_offset_right: float
    cw_blockage_threshold: float
    distance_rear_axle: int
    wheelbase: int
    steering_gear_ratio: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., oversteer_understeer: _Optional[int] = ..., yaw_rate_bias_shift: bool = ..., beamwidth_vert: _Optional[float] = ..., funnel_offset_left: _Optional[float] = ..., funnel_offset_right: _Optional[float] = ..., cw_blockage_threshold: _Optional[float] = ..., distance_rear_axle: _Optional[int] = ..., wheelbase: _Optional[int] = ..., steering_gear_ratio: _Optional[float] = ...) -> None: ...
