from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.ublox_msgs.msg import esf_raw_block_pb2 as _esf_raw_block_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EsfRAW(_message.Message):
    __slots__ = ("header", "reserved0", "blocks")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    RESERVED0_FIELD_NUMBER: _ClassVar[int]
    BLOCKS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    reserved0: _containers.RepeatedScalarFieldContainer[int]
    blocks: _containers.RepeatedCompositeFieldContainer[_esf_raw_block_pb2.EsfRAWBlock]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., reserved0: _Optional[_Iterable[int]] = ..., blocks: _Optional[_Iterable[_Union[_esf_raw_block_pb2.EsfRAWBlock, _Mapping]]] = ...) -> None: ...
