from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CfgPRT(_message.Message):
    __slots__ = ("header", "port_id", "reserved0", "tx_ready", "mode", "baud_rate", "in_proto_mask", "out_proto_mask", "flags", "reserved1")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PORT_ID_FIELD_NUMBER: _ClassVar[int]
    RESERVED0_FIELD_NUMBER: _ClassVar[int]
    TX_READY_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    BAUD_RATE_FIELD_NUMBER: _ClassVar[int]
    IN_PROTO_MASK_FIELD_NUMBER: _ClassVar[int]
    OUT_PROTO_MASK_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    RESERVED1_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    port_id: int
    reserved0: int
    tx_ready: int
    mode: int
    baud_rate: int
    in_proto_mask: int
    out_proto_mask: int
    flags: int
    reserved1: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., port_id: _Optional[int] = ..., reserved0: _Optional[int] = ..., tx_ready: _Optional[int] = ..., mode: _Optional[int] = ..., baud_rate: _Optional[int] = ..., in_proto_mask: _Optional[int] = ..., out_proto_mask: _Optional[int] = ..., flags: _Optional[int] = ..., reserved1: _Optional[int] = ...) -> None: ...
