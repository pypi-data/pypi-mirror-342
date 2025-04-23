from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NavRELPOSNED9(_message.Message):
    __slots__ = ("header", "version", "reserved1", "ref_station_id", "i_tow", "rel_pos_n", "rel_pos_e", "rel_pos_d", "rel_pos_length", "rel_pos_heading", "reserved2", "rel_pos_hpn", "rel_pos_hpe", "rel_pos_hpd", "rel_pos_hp_length", "acc_n", "acc_e", "acc_d", "acc_length", "acc_heading", "reserved3", "flags")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    RESERVED1_FIELD_NUMBER: _ClassVar[int]
    REF_STATION_ID_FIELD_NUMBER: _ClassVar[int]
    I_TOW_FIELD_NUMBER: _ClassVar[int]
    REL_POS_N_FIELD_NUMBER: _ClassVar[int]
    REL_POS_E_FIELD_NUMBER: _ClassVar[int]
    REL_POS_D_FIELD_NUMBER: _ClassVar[int]
    REL_POS_LENGTH_FIELD_NUMBER: _ClassVar[int]
    REL_POS_HEADING_FIELD_NUMBER: _ClassVar[int]
    RESERVED2_FIELD_NUMBER: _ClassVar[int]
    REL_POS_HPN_FIELD_NUMBER: _ClassVar[int]
    REL_POS_HPE_FIELD_NUMBER: _ClassVar[int]
    REL_POS_HPD_FIELD_NUMBER: _ClassVar[int]
    REL_POS_HP_LENGTH_FIELD_NUMBER: _ClassVar[int]
    ACC_N_FIELD_NUMBER: _ClassVar[int]
    ACC_E_FIELD_NUMBER: _ClassVar[int]
    ACC_D_FIELD_NUMBER: _ClassVar[int]
    ACC_LENGTH_FIELD_NUMBER: _ClassVar[int]
    ACC_HEADING_FIELD_NUMBER: _ClassVar[int]
    RESERVED3_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    version: int
    reserved1: int
    ref_station_id: int
    i_tow: int
    rel_pos_n: int
    rel_pos_e: int
    rel_pos_d: int
    rel_pos_length: int
    rel_pos_heading: int
    reserved2: _containers.RepeatedScalarFieldContainer[int]
    rel_pos_hpn: int
    rel_pos_hpe: int
    rel_pos_hpd: int
    rel_pos_hp_length: int
    acc_n: int
    acc_e: int
    acc_d: int
    acc_length: int
    acc_heading: int
    reserved3: _containers.RepeatedScalarFieldContainer[int]
    flags: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., version: _Optional[int] = ..., reserved1: _Optional[int] = ..., ref_station_id: _Optional[int] = ..., i_tow: _Optional[int] = ..., rel_pos_n: _Optional[int] = ..., rel_pos_e: _Optional[int] = ..., rel_pos_d: _Optional[int] = ..., rel_pos_length: _Optional[int] = ..., rel_pos_heading: _Optional[int] = ..., reserved2: _Optional[_Iterable[int]] = ..., rel_pos_hpn: _Optional[int] = ..., rel_pos_hpe: _Optional[int] = ..., rel_pos_hpd: _Optional[int] = ..., rel_pos_hp_length: _Optional[int] = ..., acc_n: _Optional[int] = ..., acc_e: _Optional[int] = ..., acc_d: _Optional[int] = ..., acc_length: _Optional[int] = ..., acc_heading: _Optional[int] = ..., reserved3: _Optional[_Iterable[int]] = ..., flags: _Optional[int] = ...) -> None: ...
