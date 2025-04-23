from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.ds_dbw_msgs.msg import decel_src_pb2 as _decel_src_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DriverAssist(_message.Message):
    __slots__ = ("header", "ros2_header", "decel", "decel_src", "fcw_active", "fcw_enabled", "aeb_active", "aeb_precharge", "aeb_enabled", "acc_braking", "acc_enabled", "blis_l_alert", "blis_l_enabled", "blis_r_alert", "blis_r_enabled", "cta_l_alert", "cta_l_enabled", "cta_r_alert", "cta_r_enabled")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    DECEL_FIELD_NUMBER: _ClassVar[int]
    DECEL_SRC_FIELD_NUMBER: _ClassVar[int]
    FCW_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    FCW_ENABLED_FIELD_NUMBER: _ClassVar[int]
    AEB_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    AEB_PRECHARGE_FIELD_NUMBER: _ClassVar[int]
    AEB_ENABLED_FIELD_NUMBER: _ClassVar[int]
    ACC_BRAKING_FIELD_NUMBER: _ClassVar[int]
    ACC_ENABLED_FIELD_NUMBER: _ClassVar[int]
    BLIS_L_ALERT_FIELD_NUMBER: _ClassVar[int]
    BLIS_L_ENABLED_FIELD_NUMBER: _ClassVar[int]
    BLIS_R_ALERT_FIELD_NUMBER: _ClassVar[int]
    BLIS_R_ENABLED_FIELD_NUMBER: _ClassVar[int]
    CTA_L_ALERT_FIELD_NUMBER: _ClassVar[int]
    CTA_L_ENABLED_FIELD_NUMBER: _ClassVar[int]
    CTA_R_ALERT_FIELD_NUMBER: _ClassVar[int]
    CTA_R_ENABLED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    decel: float
    decel_src: _decel_src_pb2.DecelSrc
    fcw_active: bool
    fcw_enabled: bool
    aeb_active: bool
    aeb_precharge: bool
    aeb_enabled: bool
    acc_braking: bool
    acc_enabled: bool
    blis_l_alert: bool
    blis_l_enabled: bool
    blis_r_alert: bool
    blis_r_enabled: bool
    cta_l_alert: bool
    cta_l_enabled: bool
    cta_r_alert: bool
    cta_r_enabled: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., decel: _Optional[float] = ..., decel_src: _Optional[_Union[_decel_src_pb2.DecelSrc, _Mapping]] = ..., fcw_active: bool = ..., fcw_enabled: bool = ..., aeb_active: bool = ..., aeb_precharge: bool = ..., aeb_enabled: bool = ..., acc_braking: bool = ..., acc_enabled: bool = ..., blis_l_alert: bool = ..., blis_l_enabled: bool = ..., blis_r_alert: bool = ..., blis_r_enabled: bool = ..., cta_l_alert: bool = ..., cta_l_enabled: bool = ..., cta_r_alert: bool = ..., cta_r_enabled: bool = ...) -> None: ...
