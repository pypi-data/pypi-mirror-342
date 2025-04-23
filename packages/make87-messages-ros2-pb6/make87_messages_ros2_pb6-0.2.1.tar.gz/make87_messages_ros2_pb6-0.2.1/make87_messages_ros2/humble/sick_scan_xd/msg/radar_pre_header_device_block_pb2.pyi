from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RadarPreHeaderDeviceBlock(_message.Message):
    __slots__ = ("header", "uiident", "udiserialno", "bdeviceerror", "bcontaminationwarning", "bcontaminationerror")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    UIIDENT_FIELD_NUMBER: _ClassVar[int]
    UDISERIALNO_FIELD_NUMBER: _ClassVar[int]
    BDEVICEERROR_FIELD_NUMBER: _ClassVar[int]
    BCONTAMINATIONWARNING_FIELD_NUMBER: _ClassVar[int]
    BCONTAMINATIONERROR_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    uiident: int
    udiserialno: int
    bdeviceerror: bool
    bcontaminationwarning: bool
    bcontaminationerror: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., uiident: _Optional[int] = ..., udiserialno: _Optional[int] = ..., bdeviceerror: bool = ..., bcontaminationwarning: bool = ..., bcontaminationerror: bool = ...) -> None: ...
