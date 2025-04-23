from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GimbalManagerCameraTrackRequest(_message.Message):
    __slots__ = ("mode", "x", "y", "radius", "top_left_x", "top_left_y", "bottom_right_x", "bottom_right_y")
    MODE_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    RADIUS_FIELD_NUMBER: _ClassVar[int]
    TOP_LEFT_X_FIELD_NUMBER: _ClassVar[int]
    TOP_LEFT_Y_FIELD_NUMBER: _ClassVar[int]
    BOTTOM_RIGHT_X_FIELD_NUMBER: _ClassVar[int]
    BOTTOM_RIGHT_Y_FIELD_NUMBER: _ClassVar[int]
    mode: int
    x: float
    y: float
    radius: float
    top_left_x: float
    top_left_y: float
    bottom_right_x: float
    bottom_right_y: float
    def __init__(self, mode: _Optional[int] = ..., x: _Optional[float] = ..., y: _Optional[float] = ..., radius: _Optional[float] = ..., top_left_x: _Optional[float] = ..., top_left_y: _Optional[float] = ..., bottom_right_x: _Optional[float] = ..., bottom_right_y: _Optional[float] = ...) -> None: ...

class GimbalManagerCameraTrackResponse(_message.Message):
    __slots__ = ("success", "result")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    success: bool
    result: int
    def __init__(self, success: bool = ..., result: _Optional[int] = ...) -> None: ...
