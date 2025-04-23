from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EsrVehicle3(_message.Message):
    __slots__ = ("header", "long_accel_validity", "lat_accel_validity", "lat_accel", "long_accel", "radar_fov_lr", "radar_fov_mr", "auto_align_disable", "radar_height", "serv_align_type", "serv_align_enable", "aalign_avg_ctr_total", "auto_align_converged", "wheel_slip", "serv_align_updates_need", "angle_mounting_offset")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LONG_ACCEL_VALIDITY_FIELD_NUMBER: _ClassVar[int]
    LAT_ACCEL_VALIDITY_FIELD_NUMBER: _ClassVar[int]
    LAT_ACCEL_FIELD_NUMBER: _ClassVar[int]
    LONG_ACCEL_FIELD_NUMBER: _ClassVar[int]
    RADAR_FOV_LR_FIELD_NUMBER: _ClassVar[int]
    RADAR_FOV_MR_FIELD_NUMBER: _ClassVar[int]
    AUTO_ALIGN_DISABLE_FIELD_NUMBER: _ClassVar[int]
    RADAR_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    SERV_ALIGN_TYPE_FIELD_NUMBER: _ClassVar[int]
    SERV_ALIGN_ENABLE_FIELD_NUMBER: _ClassVar[int]
    AALIGN_AVG_CTR_TOTAL_FIELD_NUMBER: _ClassVar[int]
    AUTO_ALIGN_CONVERGED_FIELD_NUMBER: _ClassVar[int]
    WHEEL_SLIP_FIELD_NUMBER: _ClassVar[int]
    SERV_ALIGN_UPDATES_NEED_FIELD_NUMBER: _ClassVar[int]
    ANGLE_MOUNTING_OFFSET_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    long_accel_validity: bool
    lat_accel_validity: bool
    lat_accel: float
    long_accel: float
    radar_fov_lr: int
    radar_fov_mr: int
    auto_align_disable: bool
    radar_height: int
    serv_align_type: bool
    serv_align_enable: bool
    aalign_avg_ctr_total: int
    auto_align_converged: bool
    wheel_slip: int
    serv_align_updates_need: int
    angle_mounting_offset: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., long_accel_validity: bool = ..., lat_accel_validity: bool = ..., lat_accel: _Optional[float] = ..., long_accel: _Optional[float] = ..., radar_fov_lr: _Optional[int] = ..., radar_fov_mr: _Optional[int] = ..., auto_align_disable: bool = ..., radar_height: _Optional[int] = ..., serv_align_type: bool = ..., serv_align_enable: bool = ..., aalign_avg_ctr_total: _Optional[int] = ..., auto_align_converged: bool = ..., wheel_slip: _Optional[int] = ..., serv_align_updates_need: _Optional[int] = ..., angle_mounting_offset: _Optional[int] = ...) -> None: ...
