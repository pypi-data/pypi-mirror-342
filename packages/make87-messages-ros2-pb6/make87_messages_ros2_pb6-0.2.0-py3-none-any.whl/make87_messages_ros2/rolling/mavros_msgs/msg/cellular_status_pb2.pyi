from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CellularStatus(_message.Message):
    __slots__ = ("status", "failure_reason", "type", "quality", "mcc", "mnc", "lac")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    FAILURE_REASON_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    QUALITY_FIELD_NUMBER: _ClassVar[int]
    MCC_FIELD_NUMBER: _ClassVar[int]
    MNC_FIELD_NUMBER: _ClassVar[int]
    LAC_FIELD_NUMBER: _ClassVar[int]
    status: int
    failure_reason: int
    type: int
    quality: int
    mcc: int
    mnc: int
    lac: int
    def __init__(self, status: _Optional[int] = ..., failure_reason: _Optional[int] = ..., type: _Optional[int] = ..., quality: _Optional[int] = ..., mcc: _Optional[int] = ..., mnc: _Optional[int] = ..., lac: _Optional[int] = ...) -> None: ...
