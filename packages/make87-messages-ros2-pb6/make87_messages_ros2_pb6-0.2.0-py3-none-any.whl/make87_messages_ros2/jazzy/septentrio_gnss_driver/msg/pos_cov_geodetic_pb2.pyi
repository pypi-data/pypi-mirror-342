from make87_messages_ros2.jazzy.septentrio_gnss_driver.msg import block_header_pb2 as _block_header_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PosCovGeodetic(_message.Message):
    __slots__ = ("header", "block_header", "mode", "error", "cov_latlat", "cov_lonlon", "cov_hgthgt", "cov_bb", "cov_latlon", "cov_lathgt", "cov_latb", "cov_lonhgt", "cov_lonb", "cov_hb")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BLOCK_HEADER_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    COV_LATLAT_FIELD_NUMBER: _ClassVar[int]
    COV_LONLON_FIELD_NUMBER: _ClassVar[int]
    COV_HGTHGT_FIELD_NUMBER: _ClassVar[int]
    COV_BB_FIELD_NUMBER: _ClassVar[int]
    COV_LATLON_FIELD_NUMBER: _ClassVar[int]
    COV_LATHGT_FIELD_NUMBER: _ClassVar[int]
    COV_LATB_FIELD_NUMBER: _ClassVar[int]
    COV_LONHGT_FIELD_NUMBER: _ClassVar[int]
    COV_LONB_FIELD_NUMBER: _ClassVar[int]
    COV_HB_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    block_header: _block_header_pb2.BlockHeader
    mode: int
    error: int
    cov_latlat: float
    cov_lonlon: float
    cov_hgthgt: float
    cov_bb: float
    cov_latlon: float
    cov_lathgt: float
    cov_latb: float
    cov_lonhgt: float
    cov_lonb: float
    cov_hb: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., block_header: _Optional[_Union[_block_header_pb2.BlockHeader, _Mapping]] = ..., mode: _Optional[int] = ..., error: _Optional[int] = ..., cov_latlat: _Optional[float] = ..., cov_lonlon: _Optional[float] = ..., cov_hgthgt: _Optional[float] = ..., cov_bb: _Optional[float] = ..., cov_latlon: _Optional[float] = ..., cov_lathgt: _Optional[float] = ..., cov_latb: _Optional[float] = ..., cov_lonhgt: _Optional[float] = ..., cov_lonb: _Optional[float] = ..., cov_hb: _Optional[float] = ...) -> None: ...
