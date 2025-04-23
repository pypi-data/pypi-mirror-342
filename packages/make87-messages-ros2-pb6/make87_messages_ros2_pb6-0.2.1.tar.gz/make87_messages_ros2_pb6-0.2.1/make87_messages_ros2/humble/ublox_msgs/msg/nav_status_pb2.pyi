from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NavSTATUS(_message.Message):
    __slots__ = ("header", "i_tow", "gps_fix", "flags", "fix_stat", "flags2", "ttff", "msss")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    I_TOW_FIELD_NUMBER: _ClassVar[int]
    GPS_FIX_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    FIX_STAT_FIELD_NUMBER: _ClassVar[int]
    FLAGS2_FIELD_NUMBER: _ClassVar[int]
    TTFF_FIELD_NUMBER: _ClassVar[int]
    MSSS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    i_tow: int
    gps_fix: int
    flags: int
    fix_stat: int
    flags2: int
    ttff: int
    msss: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., i_tow: _Optional[int] = ..., gps_fix: _Optional[int] = ..., flags: _Optional[int] = ..., fix_stat: _Optional[int] = ..., flags2: _Optional[int] = ..., ttff: _Optional[int] = ..., msss: _Optional[int] = ...) -> None: ...
