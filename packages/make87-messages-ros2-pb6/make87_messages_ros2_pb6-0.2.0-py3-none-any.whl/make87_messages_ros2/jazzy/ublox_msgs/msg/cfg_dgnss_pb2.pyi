from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CfgDGNSS(_message.Message):
    __slots__ = ("dgnss_mode", "reserved0")
    DGNSS_MODE_FIELD_NUMBER: _ClassVar[int]
    RESERVED0_FIELD_NUMBER: _ClassVar[int]
    dgnss_mode: int
    reserved0: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, dgnss_mode: _Optional[int] = ..., reserved0: _Optional[_Iterable[int]] = ...) -> None: ...
