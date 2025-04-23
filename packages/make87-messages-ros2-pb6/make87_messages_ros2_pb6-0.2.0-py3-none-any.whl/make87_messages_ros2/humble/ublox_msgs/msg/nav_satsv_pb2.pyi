from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NavSATSV(_message.Message):
    __slots__ = ("header", "gnss_id", "sv_id", "cno", "elev", "azim", "pr_res", "flags")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    GNSS_ID_FIELD_NUMBER: _ClassVar[int]
    SV_ID_FIELD_NUMBER: _ClassVar[int]
    CNO_FIELD_NUMBER: _ClassVar[int]
    ELEV_FIELD_NUMBER: _ClassVar[int]
    AZIM_FIELD_NUMBER: _ClassVar[int]
    PR_RES_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    gnss_id: int
    sv_id: int
    cno: int
    elev: int
    azim: int
    pr_res: int
    flags: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., gnss_id: _Optional[int] = ..., sv_id: _Optional[int] = ..., cno: _Optional[int] = ..., elev: _Optional[int] = ..., azim: _Optional[int] = ..., pr_res: _Optional[int] = ..., flags: _Optional[int] = ...) -> None: ...
