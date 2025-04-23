from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RxmSFRB(_message.Message):
    __slots__ = ("header", "chn", "svid", "dwrd")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CHN_FIELD_NUMBER: _ClassVar[int]
    SVID_FIELD_NUMBER: _ClassVar[int]
    DWRD_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    chn: int
    svid: int
    dwrd: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., chn: _Optional[int] = ..., svid: _Optional[int] = ..., dwrd: _Optional[_Iterable[int]] = ...) -> None: ...
