from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RadarPreHeaderStatusBlock(_message.Message):
    __slots__ = ("header", "uitelegramcount", "uicyclecount", "udisystemcountscan", "udisystemcounttransmit", "uiinputs", "uioutputs")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    UITELEGRAMCOUNT_FIELD_NUMBER: _ClassVar[int]
    UICYCLECOUNT_FIELD_NUMBER: _ClassVar[int]
    UDISYSTEMCOUNTSCAN_FIELD_NUMBER: _ClassVar[int]
    UDISYSTEMCOUNTTRANSMIT_FIELD_NUMBER: _ClassVar[int]
    UIINPUTS_FIELD_NUMBER: _ClassVar[int]
    UIOUTPUTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    uitelegramcount: int
    uicyclecount: int
    udisystemcountscan: int
    udisystemcounttransmit: int
    uiinputs: int
    uioutputs: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., uitelegramcount: _Optional[int] = ..., uicyclecount: _Optional[int] = ..., udisystemcountscan: _Optional[int] = ..., udisystemcounttransmit: _Optional[int] = ..., uiinputs: _Optional[int] = ..., uioutputs: _Optional[int] = ...) -> None: ...
