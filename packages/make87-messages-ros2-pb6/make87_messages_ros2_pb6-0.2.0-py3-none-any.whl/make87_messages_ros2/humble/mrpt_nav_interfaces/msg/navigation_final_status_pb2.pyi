from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NavigationFinalStatus(_message.Message):
    __slots__ = ("header", "navigation_status")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NAVIGATION_STATUS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    navigation_status: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., navigation_status: _Optional[int] = ...) -> None: ...
