from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SBASSvData(_message.Message):
    __slots__ = ("header", "svid", "reserved_1", "udre", "sv_sys", "sv_service", "reserved_2", "prc", "reserved_3", "ic")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SVID_FIELD_NUMBER: _ClassVar[int]
    RESERVED_1_FIELD_NUMBER: _ClassVar[int]
    UDRE_FIELD_NUMBER: _ClassVar[int]
    SV_SYS_FIELD_NUMBER: _ClassVar[int]
    SV_SERVICE_FIELD_NUMBER: _ClassVar[int]
    RESERVED_2_FIELD_NUMBER: _ClassVar[int]
    PRC_FIELD_NUMBER: _ClassVar[int]
    RESERVED_3_FIELD_NUMBER: _ClassVar[int]
    IC_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    svid: int
    reserved_1: int
    udre: int
    sv_sys: int
    sv_service: int
    reserved_2: int
    prc: int
    reserved_3: _containers.RepeatedScalarFieldContainer[int]
    ic: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., svid: _Optional[int] = ..., reserved_1: _Optional[int] = ..., udre: _Optional[int] = ..., sv_sys: _Optional[int] = ..., sv_service: _Optional[int] = ..., reserved_2: _Optional[int] = ..., prc: _Optional[int] = ..., reserved_3: _Optional[_Iterable[int]] = ..., ic: _Optional[int] = ...) -> None: ...
