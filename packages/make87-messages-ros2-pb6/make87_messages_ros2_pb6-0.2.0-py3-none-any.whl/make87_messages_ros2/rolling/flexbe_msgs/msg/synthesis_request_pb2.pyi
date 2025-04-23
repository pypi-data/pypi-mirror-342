from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SynthesisRequest(_message.Message):
    __slots__ = ("name", "system", "goal", "initial_condition", "sm_outcomes")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_FIELD_NUMBER: _ClassVar[int]
    GOAL_FIELD_NUMBER: _ClassVar[int]
    INITIAL_CONDITION_FIELD_NUMBER: _ClassVar[int]
    SM_OUTCOMES_FIELD_NUMBER: _ClassVar[int]
    name: str
    system: str
    goal: str
    initial_condition: str
    sm_outcomes: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ..., system: _Optional[str] = ..., goal: _Optional[str] = ..., initial_condition: _Optional[str] = ..., sm_outcomes: _Optional[_Iterable[str]] = ...) -> None: ...
