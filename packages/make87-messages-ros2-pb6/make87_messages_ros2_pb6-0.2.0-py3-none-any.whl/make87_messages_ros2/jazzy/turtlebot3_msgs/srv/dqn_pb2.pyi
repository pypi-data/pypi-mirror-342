from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DqnRequest(_message.Message):
    __slots__ = ("action", "init")
    ACTION_FIELD_NUMBER: _ClassVar[int]
    INIT_FIELD_NUMBER: _ClassVar[int]
    action: int
    init: bool
    def __init__(self, action: _Optional[int] = ..., init: bool = ...) -> None: ...

class DqnResponse(_message.Message):
    __slots__ = ("state", "reward", "done")
    STATE_FIELD_NUMBER: _ClassVar[int]
    REWARD_FIELD_NUMBER: _ClassVar[int]
    DONE_FIELD_NUMBER: _ClassVar[int]
    state: _containers.RepeatedScalarFieldContainer[float]
    reward: float
    done: bool
    def __init__(self, state: _Optional[_Iterable[float]] = ..., reward: _Optional[float] = ..., done: bool = ...) -> None: ...
