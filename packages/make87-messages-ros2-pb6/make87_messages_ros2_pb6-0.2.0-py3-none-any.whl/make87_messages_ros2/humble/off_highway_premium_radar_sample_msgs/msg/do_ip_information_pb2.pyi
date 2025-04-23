from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DoIpInformation(_message.Message):
    __slots__ = ("header", "physical_address", "functional_address", "target_address")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PHYSICAL_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    FUNCTIONAL_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    TARGET_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    physical_address: int
    functional_address: int
    target_address: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., physical_address: _Optional[int] = ..., functional_address: _Optional[int] = ..., target_address: _Optional[int] = ...) -> None: ...
