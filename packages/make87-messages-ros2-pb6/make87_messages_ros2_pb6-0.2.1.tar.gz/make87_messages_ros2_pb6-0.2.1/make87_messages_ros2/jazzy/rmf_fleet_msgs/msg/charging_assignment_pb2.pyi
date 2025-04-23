from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ChargingAssignment(_message.Message):
    __slots__ = ("robot_name", "waypoint_name", "mode")
    ROBOT_NAME_FIELD_NUMBER: _ClassVar[int]
    WAYPOINT_NAME_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    robot_name: str
    waypoint_name: str
    mode: int
    def __init__(self, robot_name: _Optional[str] = ..., waypoint_name: _Optional[str] = ..., mode: _Optional[int] = ...) -> None: ...
