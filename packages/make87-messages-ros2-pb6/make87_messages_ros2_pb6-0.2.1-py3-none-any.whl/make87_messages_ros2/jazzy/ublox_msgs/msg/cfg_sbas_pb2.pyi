from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CfgSBAS(_message.Message):
    __slots__ = ("mode", "usage", "max_sbas", "scanmode2", "scanmode1")
    MODE_FIELD_NUMBER: _ClassVar[int]
    USAGE_FIELD_NUMBER: _ClassVar[int]
    MAX_SBAS_FIELD_NUMBER: _ClassVar[int]
    SCANMODE2_FIELD_NUMBER: _ClassVar[int]
    SCANMODE1_FIELD_NUMBER: _ClassVar[int]
    mode: int
    usage: int
    max_sbas: int
    scanmode2: int
    scanmode1: int
    def __init__(self, mode: _Optional[int] = ..., usage: _Optional[int] = ..., max_sbas: _Optional[int] = ..., scanmode2: _Optional[int] = ..., scanmode1: _Optional[int] = ...) -> None: ...
