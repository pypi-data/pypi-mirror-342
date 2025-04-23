from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class JointRequestRequest(_message.Message):
    __slots__ = ("joint_name",)
    JOINT_NAME_FIELD_NUMBER: _ClassVar[int]
    joint_name: str
    def __init__(self, joint_name: _Optional[str] = ...) -> None: ...

class JointRequestResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
