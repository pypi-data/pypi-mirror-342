from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class NAVOdomVelocity(_message.Message):
    __slots__ = ("vel_x", "vel_y", "omega", "timestamp", "coordbase")
    VEL_X_FIELD_NUMBER: _ClassVar[int]
    VEL_Y_FIELD_NUMBER: _ClassVar[int]
    OMEGA_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    COORDBASE_FIELD_NUMBER: _ClassVar[int]
    vel_x: float
    vel_y: float
    omega: float
    timestamp: int
    coordbase: int
    def __init__(self, vel_x: _Optional[float] = ..., vel_y: _Optional[float] = ..., omega: _Optional[float] = ..., timestamp: _Optional[int] = ..., coordbase: _Optional[int] = ...) -> None: ...
