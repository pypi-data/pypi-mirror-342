from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ChronyTrackingStatus(_message.Message):
    __slots__ = ("header", "reference", "stratum", "system_time_offset", "last_offset", "rms_offset", "frequency_offset", "residual_frequency", "skew", "root_delay", "root_dispersion", "update_interval", "leap_status")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_FIELD_NUMBER: _ClassVar[int]
    STRATUM_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_TIME_OFFSET_FIELD_NUMBER: _ClassVar[int]
    LAST_OFFSET_FIELD_NUMBER: _ClassVar[int]
    RMS_OFFSET_FIELD_NUMBER: _ClassVar[int]
    FREQUENCY_OFFSET_FIELD_NUMBER: _ClassVar[int]
    RESIDUAL_FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    SKEW_FIELD_NUMBER: _ClassVar[int]
    ROOT_DELAY_FIELD_NUMBER: _ClassVar[int]
    ROOT_DISPERSION_FIELD_NUMBER: _ClassVar[int]
    UPDATE_INTERVAL_FIELD_NUMBER: _ClassVar[int]
    LEAP_STATUS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    reference: str
    stratum: int
    system_time_offset: float
    last_offset: float
    rms_offset: float
    frequency_offset: float
    residual_frequency: float
    skew: float
    root_delay: float
    root_dispersion: float
    update_interval: float
    leap_status: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., reference: _Optional[str] = ..., stratum: _Optional[int] = ..., system_time_offset: _Optional[float] = ..., last_offset: _Optional[float] = ..., rms_offset: _Optional[float] = ..., frequency_offset: _Optional[float] = ..., residual_frequency: _Optional[float] = ..., skew: _Optional[float] = ..., root_delay: _Optional[float] = ..., root_dispersion: _Optional[float] = ..., update_interval: _Optional[float] = ..., leap_status: _Optional[str] = ...) -> None: ...
