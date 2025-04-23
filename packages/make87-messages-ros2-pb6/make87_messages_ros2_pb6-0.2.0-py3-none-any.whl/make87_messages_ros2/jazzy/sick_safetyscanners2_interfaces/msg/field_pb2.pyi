from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Field(_message.Message):
    __slots__ = ("ranges", "start_angle", "angular_resolution", "protective_field")
    RANGES_FIELD_NUMBER: _ClassVar[int]
    START_ANGLE_FIELD_NUMBER: _ClassVar[int]
    ANGULAR_RESOLUTION_FIELD_NUMBER: _ClassVar[int]
    PROTECTIVE_FIELD_FIELD_NUMBER: _ClassVar[int]
    ranges: _containers.RepeatedScalarFieldContainer[float]
    start_angle: float
    angular_resolution: float
    protective_field: bool
    def __init__(self, ranges: _Optional[_Iterable[float]] = ..., start_angle: _Optional[float] = ..., angular_resolution: _Optional[float] = ..., protective_field: bool = ...) -> None: ...
