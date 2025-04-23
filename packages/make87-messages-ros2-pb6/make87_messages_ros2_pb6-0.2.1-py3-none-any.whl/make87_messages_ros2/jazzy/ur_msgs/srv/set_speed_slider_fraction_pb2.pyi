from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SetSpeedSliderFractionRequest(_message.Message):
    __slots__ = ("speed_slider_fraction",)
    SPEED_SLIDER_FRACTION_FIELD_NUMBER: _ClassVar[int]
    speed_slider_fraction: float
    def __init__(self, speed_slider_fraction: _Optional[float] = ...) -> None: ...

class SetSpeedSliderFractionResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
