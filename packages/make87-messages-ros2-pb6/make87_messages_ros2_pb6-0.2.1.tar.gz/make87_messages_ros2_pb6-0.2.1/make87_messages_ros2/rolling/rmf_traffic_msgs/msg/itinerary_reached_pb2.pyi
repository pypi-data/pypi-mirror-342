from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ItineraryReached(_message.Message):
    __slots__ = ("participant", "plan", "reached_checkpoints", "progress_version")
    PARTICIPANT_FIELD_NUMBER: _ClassVar[int]
    PLAN_FIELD_NUMBER: _ClassVar[int]
    REACHED_CHECKPOINTS_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_VERSION_FIELD_NUMBER: _ClassVar[int]
    participant: int
    plan: int
    reached_checkpoints: _containers.RepeatedScalarFieldContainer[int]
    progress_version: int
    def __init__(self, participant: _Optional[int] = ..., plan: _Optional[int] = ..., reached_checkpoints: _Optional[_Iterable[int]] = ..., progress_version: _Optional[int] = ...) -> None: ...
