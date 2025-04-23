from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CfgNAVX5(_message.Message):
    __slots__ = ("header", "version", "mask1", "mask2", "reserved1", "min_svs", "max_svs", "min_cno", "reserved2", "ini_fix3d", "reserved3", "ack_aiding", "wkn_rollover", "sig_atten_comp_mode", "reserved4", "use_ppp", "aop_cfg", "reserved5", "aop_orb_max_err", "reserved6", "use_adr")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    MASK1_FIELD_NUMBER: _ClassVar[int]
    MASK2_FIELD_NUMBER: _ClassVar[int]
    RESERVED1_FIELD_NUMBER: _ClassVar[int]
    MIN_SVS_FIELD_NUMBER: _ClassVar[int]
    MAX_SVS_FIELD_NUMBER: _ClassVar[int]
    MIN_CNO_FIELD_NUMBER: _ClassVar[int]
    RESERVED2_FIELD_NUMBER: _ClassVar[int]
    INI_FIX3D_FIELD_NUMBER: _ClassVar[int]
    RESERVED3_FIELD_NUMBER: _ClassVar[int]
    ACK_AIDING_FIELD_NUMBER: _ClassVar[int]
    WKN_ROLLOVER_FIELD_NUMBER: _ClassVar[int]
    SIG_ATTEN_COMP_MODE_FIELD_NUMBER: _ClassVar[int]
    RESERVED4_FIELD_NUMBER: _ClassVar[int]
    USE_PPP_FIELD_NUMBER: _ClassVar[int]
    AOP_CFG_FIELD_NUMBER: _ClassVar[int]
    RESERVED5_FIELD_NUMBER: _ClassVar[int]
    AOP_ORB_MAX_ERR_FIELD_NUMBER: _ClassVar[int]
    RESERVED6_FIELD_NUMBER: _ClassVar[int]
    USE_ADR_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    version: int
    mask1: int
    mask2: int
    reserved1: _containers.RepeatedScalarFieldContainer[int]
    min_svs: int
    max_svs: int
    min_cno: int
    reserved2: int
    ini_fix3d: int
    reserved3: _containers.RepeatedScalarFieldContainer[int]
    ack_aiding: int
    wkn_rollover: int
    sig_atten_comp_mode: int
    reserved4: _containers.RepeatedScalarFieldContainer[int]
    use_ppp: int
    aop_cfg: int
    reserved5: _containers.RepeatedScalarFieldContainer[int]
    aop_orb_max_err: int
    reserved6: _containers.RepeatedScalarFieldContainer[int]
    use_adr: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., version: _Optional[int] = ..., mask1: _Optional[int] = ..., mask2: _Optional[int] = ..., reserved1: _Optional[_Iterable[int]] = ..., min_svs: _Optional[int] = ..., max_svs: _Optional[int] = ..., min_cno: _Optional[int] = ..., reserved2: _Optional[int] = ..., ini_fix3d: _Optional[int] = ..., reserved3: _Optional[_Iterable[int]] = ..., ack_aiding: _Optional[int] = ..., wkn_rollover: _Optional[int] = ..., sig_atten_comp_mode: _Optional[int] = ..., reserved4: _Optional[_Iterable[int]] = ..., use_ppp: _Optional[int] = ..., aop_cfg: _Optional[int] = ..., reserved5: _Optional[_Iterable[int]] = ..., aop_orb_max_err: _Optional[int] = ..., reserved6: _Optional[_Iterable[int]] = ..., use_adr: _Optional[int] = ...) -> None: ...
