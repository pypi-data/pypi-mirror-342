from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from make87_messages_ros2.rolling.ublox_ubx_msgs.msg import utc_std_pb2 as _utc_std_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UBXNavTimeUTC(_message.Message):
    __slots__ = ("header", "itow", "t_acc", "nano", "year", "month", "day", "hour", "min", "sec", "valid_tow", "valid_wkn", "valid_utc", "utc_std")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ITOW_FIELD_NUMBER: _ClassVar[int]
    T_ACC_FIELD_NUMBER: _ClassVar[int]
    NANO_FIELD_NUMBER: _ClassVar[int]
    YEAR_FIELD_NUMBER: _ClassVar[int]
    MONTH_FIELD_NUMBER: _ClassVar[int]
    DAY_FIELD_NUMBER: _ClassVar[int]
    HOUR_FIELD_NUMBER: _ClassVar[int]
    MIN_FIELD_NUMBER: _ClassVar[int]
    SEC_FIELD_NUMBER: _ClassVar[int]
    VALID_TOW_FIELD_NUMBER: _ClassVar[int]
    VALID_WKN_FIELD_NUMBER: _ClassVar[int]
    VALID_UTC_FIELD_NUMBER: _ClassVar[int]
    UTC_STD_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    itow: int
    t_acc: int
    nano: int
    year: int
    month: int
    day: int
    hour: int
    min: int
    sec: int
    valid_tow: bool
    valid_wkn: bool
    valid_utc: bool
    utc_std: _utc_std_pb2.UtcStd
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., itow: _Optional[int] = ..., t_acc: _Optional[int] = ..., nano: _Optional[int] = ..., year: _Optional[int] = ..., month: _Optional[int] = ..., day: _Optional[int] = ..., hour: _Optional[int] = ..., min: _Optional[int] = ..., sec: _Optional[int] = ..., valid_tow: bool = ..., valid_wkn: bool = ..., valid_utc: bool = ..., utc_std: _Optional[_Union[_utc_std_pb2.UtcStd, _Mapping]] = ...) -> None: ...
