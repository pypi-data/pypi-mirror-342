from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class OutcomeCondition(_message.Message):
    __slots__ = ("state_name", "state_outcome")
    STATE_NAME_FIELD_NUMBER: _ClassVar[int]
    STATE_OUTCOME_FIELD_NUMBER: _ClassVar[int]
    state_name: _containers.RepeatedScalarFieldContainer[str]
    state_outcome: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, state_name: _Optional[_Iterable[str]] = ..., state_outcome: _Optional[_Iterable[str]] = ...) -> None: ...
