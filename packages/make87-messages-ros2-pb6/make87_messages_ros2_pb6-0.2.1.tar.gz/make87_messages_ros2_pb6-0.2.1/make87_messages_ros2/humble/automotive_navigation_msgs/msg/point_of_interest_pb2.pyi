from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PointOfInterest(_message.Message):
    __slots__ = ("header", "guid", "latitude", "longitude", "params")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    GUID_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    guid: int
    latitude: float
    longitude: float
    params: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., guid: _Optional[int] = ..., latitude: _Optional[float] = ..., longitude: _Optional[float] = ..., params: _Optional[str] = ...) -> None: ...
