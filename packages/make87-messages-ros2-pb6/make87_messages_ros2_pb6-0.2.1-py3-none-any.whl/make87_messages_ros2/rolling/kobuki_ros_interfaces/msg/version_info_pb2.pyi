from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class VersionInfo(_message.Message):
    __slots__ = ("hardware", "firmware", "software", "udid", "features")
    HARDWARE_FIELD_NUMBER: _ClassVar[int]
    FIRMWARE_FIELD_NUMBER: _ClassVar[int]
    SOFTWARE_FIELD_NUMBER: _ClassVar[int]
    UDID_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    hardware: str
    firmware: str
    software: str
    udid: _containers.RepeatedScalarFieldContainer[int]
    features: int
    def __init__(self, hardware: _Optional[str] = ..., firmware: _Optional[str] = ..., software: _Optional[str] = ..., udid: _Optional[_Iterable[int]] = ..., features: _Optional[int] = ...) -> None: ...
