from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class NavigationFinalStatus(_message.Message):
    __slots__ = ("navigation_status",)
    NAVIGATION_STATUS_FIELD_NUMBER: _ClassVar[int]
    navigation_status: int
    def __init__(self, navigation_status: _Optional[int] = ...) -> None: ...
