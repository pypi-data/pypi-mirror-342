from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ImusInfo(_message.Message):
    __slots__ = ("header", "sensor_ids", "battery_level", "temperature")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SENSOR_IDS_FIELD_NUMBER: _ClassVar[int]
    BATTERY_LEVEL_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    sensor_ids: _containers.RepeatedScalarFieldContainer[str]
    battery_level: float
    temperature: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., sensor_ids: _Optional[_Iterable[str]] = ..., battery_level: _Optional[float] = ..., temperature: _Optional[float] = ...) -> None: ...
