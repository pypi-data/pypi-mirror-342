from make87_messages_ros2.rolling.septentrio_gnss_driver.msg import block_header_pb2 as _block_header_pb2
from make87_messages_ros2.rolling.septentrio_gnss_driver.msg import rf_band_pb2 as _rf_band_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RFStatus(_message.Message):
    __slots__ = ("header", "block_header", "n", "sb_length", "flags", "rfband")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BLOCK_HEADER_FIELD_NUMBER: _ClassVar[int]
    N_FIELD_NUMBER: _ClassVar[int]
    SB_LENGTH_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    RFBAND_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    block_header: _block_header_pb2.BlockHeader
    n: int
    sb_length: int
    flags: int
    rfband: _containers.RepeatedCompositeFieldContainer[_rf_band_pb2.RFBand]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., block_header: _Optional[_Union[_block_header_pb2.BlockHeader, _Mapping]] = ..., n: _Optional[int] = ..., sb_length: _Optional[int] = ..., flags: _Optional[int] = ..., rfband: _Optional[_Iterable[_Union[_rf_band_pb2.RFBand, _Mapping]]] = ...) -> None: ...
