from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ReloadControllerLibrariesRequest(_message.Message):
    __slots__ = ("force_kill",)
    FORCE_KILL_FIELD_NUMBER: _ClassVar[int]
    force_kill: bool
    def __init__(self, force_kill: bool = ...) -> None: ...

class ReloadControllerLibrariesResponse(_message.Message):
    __slots__ = ("ok",)
    OK_FIELD_NUMBER: _ClassVar[int]
    ok: bool
    def __init__(self, ok: bool = ...) -> None: ...
