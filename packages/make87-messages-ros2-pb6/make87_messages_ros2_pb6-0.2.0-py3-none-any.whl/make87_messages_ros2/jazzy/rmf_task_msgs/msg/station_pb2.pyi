from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Station(_message.Message):
    __slots__ = ("task_id", "robot_type", "place_name")
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    ROBOT_TYPE_FIELD_NUMBER: _ClassVar[int]
    PLACE_NAME_FIELD_NUMBER: _ClassVar[int]
    task_id: str
    robot_type: str
    place_name: str
    def __init__(self, task_id: _Optional[str] = ..., robot_type: _Optional[str] = ..., place_name: _Optional[str] = ...) -> None: ...
