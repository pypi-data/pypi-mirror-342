from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class UserDisplay(_message.Message):
    __slots__ = ("ip", "battery", "entries", "selected_entry")
    IP_FIELD_NUMBER: _ClassVar[int]
    BATTERY_FIELD_NUMBER: _ClassVar[int]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    SELECTED_ENTRY_FIELD_NUMBER: _ClassVar[int]
    ip: str
    battery: str
    entries: _containers.RepeatedScalarFieldContainer[str]
    selected_entry: int
    def __init__(self, ip: _Optional[str] = ..., battery: _Optional[str] = ..., entries: _Optional[_Iterable[str]] = ..., selected_entry: _Optional[int] = ...) -> None: ...
