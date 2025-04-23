from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RxmSVSISV(_message.Message):
    __slots__ = ("header", "svid", "sv_flag", "azim", "elev", "age")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SVID_FIELD_NUMBER: _ClassVar[int]
    SV_FLAG_FIELD_NUMBER: _ClassVar[int]
    AZIM_FIELD_NUMBER: _ClassVar[int]
    ELEV_FIELD_NUMBER: _ClassVar[int]
    AGE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    svid: int
    sv_flag: int
    azim: int
    elev: int
    age: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., svid: _Optional[int] = ..., sv_flag: _Optional[int] = ..., azim: _Optional[int] = ..., elev: _Optional[int] = ..., age: _Optional[int] = ...) -> None: ...
