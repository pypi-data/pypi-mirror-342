from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GPS(_message.Message):
    __slots__ = ("header", "stamp", "longitude", "latitude", "altitude", "error", "bearing")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STAMP_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    BEARING_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    stamp: float
    longitude: float
    latitude: float
    altitude: float
    error: float
    bearing: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., stamp: _Optional[float] = ..., longitude: _Optional[float] = ..., latitude: _Optional[float] = ..., altitude: _Optional[float] = ..., error: _Optional[float] = ..., bearing: _Optional[float] = ...) -> None: ...
