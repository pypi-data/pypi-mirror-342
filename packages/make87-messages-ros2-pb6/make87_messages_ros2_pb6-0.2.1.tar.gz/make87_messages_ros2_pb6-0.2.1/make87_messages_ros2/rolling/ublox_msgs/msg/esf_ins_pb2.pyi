from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class EsfINS(_message.Message):
    __slots__ = ("bitfield0", "reserved1", "i_tow", "x_ang_rate", "y_ang_rate", "z_ang_rate", "x_accel", "y_accel", "z_accel")
    BITFIELD0_FIELD_NUMBER: _ClassVar[int]
    RESERVED1_FIELD_NUMBER: _ClassVar[int]
    I_TOW_FIELD_NUMBER: _ClassVar[int]
    X_ANG_RATE_FIELD_NUMBER: _ClassVar[int]
    Y_ANG_RATE_FIELD_NUMBER: _ClassVar[int]
    Z_ANG_RATE_FIELD_NUMBER: _ClassVar[int]
    X_ACCEL_FIELD_NUMBER: _ClassVar[int]
    Y_ACCEL_FIELD_NUMBER: _ClassVar[int]
    Z_ACCEL_FIELD_NUMBER: _ClassVar[int]
    bitfield0: int
    reserved1: _containers.RepeatedScalarFieldContainer[int]
    i_tow: int
    x_ang_rate: int
    y_ang_rate: int
    z_ang_rate: int
    x_accel: int
    y_accel: int
    z_accel: int
    def __init__(self, bitfield0: _Optional[int] = ..., reserved1: _Optional[_Iterable[int]] = ..., i_tow: _Optional[int] = ..., x_ang_rate: _Optional[int] = ..., y_ang_rate: _Optional[int] = ..., z_ang_rate: _Optional[int] = ..., x_accel: _Optional[int] = ..., y_accel: _Optional[int] = ..., z_accel: _Optional[int] = ...) -> None: ...
