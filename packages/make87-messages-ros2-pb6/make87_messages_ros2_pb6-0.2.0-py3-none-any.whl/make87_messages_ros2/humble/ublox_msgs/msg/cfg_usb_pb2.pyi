from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CfgUSB(_message.Message):
    __slots__ = ("header", "vendor_id", "product_id", "reserved1", "reserved2", "power_consumption", "flags", "vendor_string", "product_string", "serial_number")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    VENDOR_ID_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_ID_FIELD_NUMBER: _ClassVar[int]
    RESERVED1_FIELD_NUMBER: _ClassVar[int]
    RESERVED2_FIELD_NUMBER: _ClassVar[int]
    POWER_CONSUMPTION_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    VENDOR_STRING_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_STRING_FIELD_NUMBER: _ClassVar[int]
    SERIAL_NUMBER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    vendor_id: int
    product_id: int
    reserved1: _containers.RepeatedScalarFieldContainer[int]
    reserved2: _containers.RepeatedScalarFieldContainer[int]
    power_consumption: int
    flags: int
    vendor_string: _containers.RepeatedScalarFieldContainer[int]
    product_string: _containers.RepeatedScalarFieldContainer[int]
    serial_number: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., vendor_id: _Optional[int] = ..., product_id: _Optional[int] = ..., reserved1: _Optional[_Iterable[int]] = ..., reserved2: _Optional[_Iterable[int]] = ..., power_consumption: _Optional[int] = ..., flags: _Optional[int] = ..., vendor_string: _Optional[_Iterable[int]] = ..., product_string: _Optional[_Iterable[int]] = ..., serial_number: _Optional[_Iterable[int]] = ...) -> None: ...
