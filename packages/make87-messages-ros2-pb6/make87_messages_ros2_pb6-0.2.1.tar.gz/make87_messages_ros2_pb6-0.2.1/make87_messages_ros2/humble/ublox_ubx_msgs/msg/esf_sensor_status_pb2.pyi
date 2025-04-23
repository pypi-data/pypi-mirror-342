from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ESFSensorStatus(_message.Message):
    __slots__ = ("header", "sensor_data_type", "used", "ready", "calib_status", "time_status", "freq", "fault_bad_meas", "fault_bad_ttag", "fault_missing_meas", "fault_noisy_meas")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SENSOR_DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    USED_FIELD_NUMBER: _ClassVar[int]
    READY_FIELD_NUMBER: _ClassVar[int]
    CALIB_STATUS_FIELD_NUMBER: _ClassVar[int]
    TIME_STATUS_FIELD_NUMBER: _ClassVar[int]
    FREQ_FIELD_NUMBER: _ClassVar[int]
    FAULT_BAD_MEAS_FIELD_NUMBER: _ClassVar[int]
    FAULT_BAD_TTAG_FIELD_NUMBER: _ClassVar[int]
    FAULT_MISSING_MEAS_FIELD_NUMBER: _ClassVar[int]
    FAULT_NOISY_MEAS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    sensor_data_type: int
    used: bool
    ready: bool
    calib_status: int
    time_status: int
    freq: int
    fault_bad_meas: bool
    fault_bad_ttag: bool
    fault_missing_meas: bool
    fault_noisy_meas: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., sensor_data_type: _Optional[int] = ..., used: bool = ..., ready: bool = ..., calib_status: _Optional[int] = ..., time_status: _Optional[int] = ..., freq: _Optional[int] = ..., fault_bad_meas: bool = ..., fault_bad_ttag: bool = ..., fault_missing_meas: bool = ..., fault_noisy_meas: bool = ...) -> None: ...
