from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ScanPoint(_message.Message):
    __slots__ = ("angle", "distance", "reflectivity", "valid", "infinite", "glare", "reflector", "contamination", "contamination_warning")
    ANGLE_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_FIELD_NUMBER: _ClassVar[int]
    REFLECTIVITY_FIELD_NUMBER: _ClassVar[int]
    VALID_FIELD_NUMBER: _ClassVar[int]
    INFINITE_FIELD_NUMBER: _ClassVar[int]
    GLARE_FIELD_NUMBER: _ClassVar[int]
    REFLECTOR_FIELD_NUMBER: _ClassVar[int]
    CONTAMINATION_FIELD_NUMBER: _ClassVar[int]
    CONTAMINATION_WARNING_FIELD_NUMBER: _ClassVar[int]
    angle: float
    distance: int
    reflectivity: int
    valid: bool
    infinite: bool
    glare: bool
    reflector: bool
    contamination: bool
    contamination_warning: bool
    def __init__(self, angle: _Optional[float] = ..., distance: _Optional[int] = ..., reflectivity: _Optional[int] = ..., valid: bool = ..., infinite: bool = ..., glare: bool = ..., reflector: bool = ..., contamination: bool = ..., contamination_warning: bool = ...) -> None: ...
