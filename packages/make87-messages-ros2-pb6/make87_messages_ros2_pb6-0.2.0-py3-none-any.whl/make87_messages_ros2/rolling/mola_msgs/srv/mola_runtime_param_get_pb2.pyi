from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class MolaRuntimeParamGetRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MolaRuntimeParamGetResponse(_message.Message):
    __slots__ = ("parameters",)
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    parameters: str
    def __init__(self, parameters: _Optional[str] = ...) -> None: ...
