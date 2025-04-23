from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VehicleStateMsg3(_message.Message):
    __slots__ = ("header", "yaw_rate_reference_valid", "yaw_rate_reference", "can_veh_long_accel_qf", "can_veh_long_accel")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    YAW_RATE_REFERENCE_VALID_FIELD_NUMBER: _ClassVar[int]
    YAW_RATE_REFERENCE_FIELD_NUMBER: _ClassVar[int]
    CAN_VEH_LONG_ACCEL_QF_FIELD_NUMBER: _ClassVar[int]
    CAN_VEH_LONG_ACCEL_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    yaw_rate_reference_valid: bool
    yaw_rate_reference: float
    can_veh_long_accel_qf: int
    can_veh_long_accel: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., yaw_rate_reference_valid: bool = ..., yaw_rate_reference: _Optional[float] = ..., can_veh_long_accel_qf: _Optional[int] = ..., can_veh_long_accel: _Optional[float] = ...) -> None: ...
