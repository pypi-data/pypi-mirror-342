from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RxmSFRB(_message.Message):
    __slots__ = ("chn", "svid", "dwrd")
    CHN_FIELD_NUMBER: _ClassVar[int]
    SVID_FIELD_NUMBER: _ClassVar[int]
    DWRD_FIELD_NUMBER: _ClassVar[int]
    chn: int
    svid: int
    dwrd: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, chn: _Optional[int] = ..., svid: _Optional[int] = ..., dwrd: _Optional[_Iterable[int]] = ...) -> None: ...
