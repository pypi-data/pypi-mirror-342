from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PointOfInterestStatus(_message.Message):
    __slots__ = ("guid", "distance", "heading", "x_position", "y_position", "params")
    GUID_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_FIELD_NUMBER: _ClassVar[int]
    HEADING_FIELD_NUMBER: _ClassVar[int]
    X_POSITION_FIELD_NUMBER: _ClassVar[int]
    Y_POSITION_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    guid: int
    distance: float
    heading: float
    x_position: float
    y_position: float
    params: str
    def __init__(self, guid: _Optional[int] = ..., distance: _Optional[float] = ..., heading: _Optional[float] = ..., x_position: _Optional[float] = ..., y_position: _Optional[float] = ..., params: _Optional[str] = ...) -> None: ...
