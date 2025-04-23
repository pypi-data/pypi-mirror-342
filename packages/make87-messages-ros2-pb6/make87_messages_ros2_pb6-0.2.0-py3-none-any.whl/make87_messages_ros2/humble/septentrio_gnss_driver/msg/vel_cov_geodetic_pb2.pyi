from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.septentrio_gnss_driver.msg import block_header_pb2 as _block_header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VelCovGeodetic(_message.Message):
    __slots__ = ("header", "ros2_header", "block_header", "mode", "error", "cov_vnvn", "cov_veve", "cov_vuvu", "cov_dtdt", "cov_vnve", "cov_vnvu", "cov_vndt", "cov_vevu", "cov_vedt", "cov_vudt")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    BLOCK_HEADER_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    COV_VNVN_FIELD_NUMBER: _ClassVar[int]
    COV_VEVE_FIELD_NUMBER: _ClassVar[int]
    COV_VUVU_FIELD_NUMBER: _ClassVar[int]
    COV_DTDT_FIELD_NUMBER: _ClassVar[int]
    COV_VNVE_FIELD_NUMBER: _ClassVar[int]
    COV_VNVU_FIELD_NUMBER: _ClassVar[int]
    COV_VNDT_FIELD_NUMBER: _ClassVar[int]
    COV_VEVU_FIELD_NUMBER: _ClassVar[int]
    COV_VEDT_FIELD_NUMBER: _ClassVar[int]
    COV_VUDT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    block_header: _block_header_pb2.BlockHeader
    mode: int
    error: int
    cov_vnvn: float
    cov_veve: float
    cov_vuvu: float
    cov_dtdt: float
    cov_vnve: float
    cov_vnvu: float
    cov_vndt: float
    cov_vevu: float
    cov_vedt: float
    cov_vudt: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., block_header: _Optional[_Union[_block_header_pb2.BlockHeader, _Mapping]] = ..., mode: _Optional[int] = ..., error: _Optional[int] = ..., cov_vnvn: _Optional[float] = ..., cov_veve: _Optional[float] = ..., cov_vuvu: _Optional[float] = ..., cov_dtdt: _Optional[float] = ..., cov_vnve: _Optional[float] = ..., cov_vnvu: _Optional[float] = ..., cov_vndt: _Optional[float] = ..., cov_vevu: _Optional[float] = ..., cov_vedt: _Optional[float] = ..., cov_vudt: _Optional[float] = ...) -> None: ...
