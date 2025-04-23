from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CfgHNR(_message.Message):
    __slots__ = ("high_nav_rate", "reserved0")
    HIGH_NAV_RATE_FIELD_NUMBER: _ClassVar[int]
    RESERVED0_FIELD_NUMBER: _ClassVar[int]
    high_nav_rate: int
    reserved0: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, high_nav_rate: _Optional[int] = ..., reserved0: _Optional[_Iterable[int]] = ...) -> None: ...
