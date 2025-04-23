from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SBASService(_message.Message):
    __slots__ = ("ranging", "corrections", "integrity", "test_mode", "bad")
    RANGING_FIELD_NUMBER: _ClassVar[int]
    CORRECTIONS_FIELD_NUMBER: _ClassVar[int]
    INTEGRITY_FIELD_NUMBER: _ClassVar[int]
    TEST_MODE_FIELD_NUMBER: _ClassVar[int]
    BAD_FIELD_NUMBER: _ClassVar[int]
    ranging: bool
    corrections: bool
    integrity: bool
    test_mode: bool
    bad: bool
    def __init__(self, ranging: bool = ..., corrections: bool = ..., integrity: bool = ..., test_mode: bool = ..., bad: bool = ...) -> None: ...
