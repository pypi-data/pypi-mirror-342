from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RxmEPH(_message.Message):
    __slots__ = ("header", "svid", "how", "sf1d", "sf2d", "sf3d")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SVID_FIELD_NUMBER: _ClassVar[int]
    HOW_FIELD_NUMBER: _ClassVar[int]
    SF1D_FIELD_NUMBER: _ClassVar[int]
    SF2D_FIELD_NUMBER: _ClassVar[int]
    SF3D_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    svid: int
    how: int
    sf1d: _containers.RepeatedScalarFieldContainer[int]
    sf2d: _containers.RepeatedScalarFieldContainer[int]
    sf3d: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., svid: _Optional[int] = ..., how: _Optional[int] = ..., sf1d: _Optional[_Iterable[int]] = ..., sf2d: _Optional[_Iterable[int]] = ..., sf3d: _Optional[_Iterable[int]] = ...) -> None: ...
