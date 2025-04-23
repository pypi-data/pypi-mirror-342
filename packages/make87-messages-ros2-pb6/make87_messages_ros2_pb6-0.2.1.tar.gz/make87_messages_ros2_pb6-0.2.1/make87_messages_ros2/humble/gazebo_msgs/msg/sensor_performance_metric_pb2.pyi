from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SensorPerformanceMetric(_message.Message):
    __slots__ = ("header", "name", "sim_update_rate", "real_update_rate", "fps")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SIM_UPDATE_RATE_FIELD_NUMBER: _ClassVar[int]
    REAL_UPDATE_RATE_FIELD_NUMBER: _ClassVar[int]
    FPS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    name: str
    sim_update_rate: float
    real_update_rate: float
    fps: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., name: _Optional[str] = ..., sim_update_rate: _Optional[float] = ..., real_update_rate: _Optional[float] = ..., fps: _Optional[float] = ...) -> None: ...
