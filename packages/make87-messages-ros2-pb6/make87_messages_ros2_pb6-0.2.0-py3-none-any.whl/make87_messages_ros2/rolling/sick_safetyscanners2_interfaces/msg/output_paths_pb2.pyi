from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class OutputPaths(_message.Message):
    __slots__ = ("status", "is_safe", "is_valid", "active_monitoring_case")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    IS_SAFE_FIELD_NUMBER: _ClassVar[int]
    IS_VALID_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_MONITORING_CASE_FIELD_NUMBER: _ClassVar[int]
    status: _containers.RepeatedScalarFieldContainer[bool]
    is_safe: _containers.RepeatedScalarFieldContainer[bool]
    is_valid: _containers.RepeatedScalarFieldContainer[bool]
    active_monitoring_case: int
    def __init__(self, status: _Optional[_Iterable[bool]] = ..., is_safe: _Optional[_Iterable[bool]] = ..., is_valid: _Optional[_Iterable[bool]] = ..., active_monitoring_case: _Optional[int] = ...) -> None: ...
