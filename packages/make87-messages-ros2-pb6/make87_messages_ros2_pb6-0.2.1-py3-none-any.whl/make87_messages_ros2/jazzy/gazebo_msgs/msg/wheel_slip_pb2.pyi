from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class WheelSlip(_message.Message):
    __slots__ = ("name", "lateral_slip", "longitudinal_slip")
    NAME_FIELD_NUMBER: _ClassVar[int]
    LATERAL_SLIP_FIELD_NUMBER: _ClassVar[int]
    LONGITUDINAL_SLIP_FIELD_NUMBER: _ClassVar[int]
    name: _containers.RepeatedScalarFieldContainer[str]
    lateral_slip: _containers.RepeatedScalarFieldContainer[float]
    longitudinal_slip: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, name: _Optional[_Iterable[str]] = ..., lateral_slip: _Optional[_Iterable[float]] = ..., longitudinal_slip: _Optional[_Iterable[float]] = ...) -> None: ...
