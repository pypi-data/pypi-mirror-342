from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DispenserRequestItem(_message.Message):
    __slots__ = ("header", "type_guid", "quantity", "compartment_name")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TYPE_GUID_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    COMPARTMENT_NAME_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    type_guid: str
    quantity: int
    compartment_name: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., type_guid: _Optional[str] = ..., quantity: _Optional[int] = ..., compartment_name: _Optional[str] = ...) -> None: ...
