from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HnrPVT(_message.Message):
    __slots__ = ("header", "i_tow", "year", "month", "day", "hour", "min", "sec", "valid", "nano", "gps_fix", "flags", "reserved0", "lon", "lat", "height", "h_msl", "g_speed", "speed", "head_mot", "head_veh", "h_acc", "v_acc", "s_acc", "head_acc", "reserved1")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    I_TOW_FIELD_NUMBER: _ClassVar[int]
    YEAR_FIELD_NUMBER: _ClassVar[int]
    MONTH_FIELD_NUMBER: _ClassVar[int]
    DAY_FIELD_NUMBER: _ClassVar[int]
    HOUR_FIELD_NUMBER: _ClassVar[int]
    MIN_FIELD_NUMBER: _ClassVar[int]
    SEC_FIELD_NUMBER: _ClassVar[int]
    VALID_FIELD_NUMBER: _ClassVar[int]
    NANO_FIELD_NUMBER: _ClassVar[int]
    GPS_FIX_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    RESERVED0_FIELD_NUMBER: _ClassVar[int]
    LON_FIELD_NUMBER: _ClassVar[int]
    LAT_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    H_MSL_FIELD_NUMBER: _ClassVar[int]
    G_SPEED_FIELD_NUMBER: _ClassVar[int]
    SPEED_FIELD_NUMBER: _ClassVar[int]
    HEAD_MOT_FIELD_NUMBER: _ClassVar[int]
    HEAD_VEH_FIELD_NUMBER: _ClassVar[int]
    H_ACC_FIELD_NUMBER: _ClassVar[int]
    V_ACC_FIELD_NUMBER: _ClassVar[int]
    S_ACC_FIELD_NUMBER: _ClassVar[int]
    HEAD_ACC_FIELD_NUMBER: _ClassVar[int]
    RESERVED1_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    i_tow: int
    year: int
    month: int
    day: int
    hour: int
    min: int
    sec: int
    valid: int
    nano: int
    gps_fix: int
    flags: int
    reserved0: _containers.RepeatedScalarFieldContainer[int]
    lon: int
    lat: int
    height: int
    h_msl: int
    g_speed: int
    speed: int
    head_mot: int
    head_veh: int
    h_acc: int
    v_acc: int
    s_acc: int
    head_acc: int
    reserved1: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., i_tow: _Optional[int] = ..., year: _Optional[int] = ..., month: _Optional[int] = ..., day: _Optional[int] = ..., hour: _Optional[int] = ..., min: _Optional[int] = ..., sec: _Optional[int] = ..., valid: _Optional[int] = ..., nano: _Optional[int] = ..., gps_fix: _Optional[int] = ..., flags: _Optional[int] = ..., reserved0: _Optional[_Iterable[int]] = ..., lon: _Optional[int] = ..., lat: _Optional[int] = ..., height: _Optional[int] = ..., h_msl: _Optional[int] = ..., g_speed: _Optional[int] = ..., speed: _Optional[int] = ..., head_mot: _Optional[int] = ..., head_veh: _Optional[int] = ..., h_acc: _Optional[int] = ..., v_acc: _Optional[int] = ..., s_acc: _Optional[int] = ..., head_acc: _Optional[int] = ..., reserved1: _Optional[_Iterable[int]] = ...) -> None: ...
