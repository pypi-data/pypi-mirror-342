from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class InterruptRequest(_message.Message):
    __slots__ = ("fleet_name", "robot_name", "interrupt_id", "labels", "type")
    FLEET_NAME_FIELD_NUMBER: _ClassVar[int]
    ROBOT_NAME_FIELD_NUMBER: _ClassVar[int]
    INTERRUPT_ID_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    fleet_name: str
    robot_name: str
    interrupt_id: str
    labels: _containers.RepeatedScalarFieldContainer[str]
    type: int
    def __init__(self, fleet_name: _Optional[str] = ..., robot_name: _Optional[str] = ..., interrupt_id: _Optional[str] = ..., labels: _Optional[_Iterable[str]] = ..., type: _Optional[int] = ...) -> None: ...
