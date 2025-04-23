from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class TrajectoryWaypoint(_message.Message):
    __slots__ = ("time", "position", "velocity")
    TIME_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_FIELD_NUMBER: _ClassVar[int]
    time: int
    position: _containers.RepeatedScalarFieldContainer[float]
    velocity: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, time: _Optional[int] = ..., position: _Optional[_Iterable[float]] = ..., velocity: _Optional[_Iterable[float]] = ...) -> None: ...
