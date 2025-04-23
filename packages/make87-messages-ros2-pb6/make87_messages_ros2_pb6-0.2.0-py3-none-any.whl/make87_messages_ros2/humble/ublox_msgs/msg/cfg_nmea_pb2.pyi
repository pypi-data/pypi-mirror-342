from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CfgNMEA(_message.Message):
    __slots__ = ("header", "filter", "nmea_version", "num_sv", "flags", "gnss_to_filter", "sv_numbering", "main_talker_id", "gsv_talker_id", "version", "bds_talker_id", "reserved1")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    NMEA_VERSION_FIELD_NUMBER: _ClassVar[int]
    NUM_SV_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    GNSS_TO_FILTER_FIELD_NUMBER: _ClassVar[int]
    SV_NUMBERING_FIELD_NUMBER: _ClassVar[int]
    MAIN_TALKER_ID_FIELD_NUMBER: _ClassVar[int]
    GSV_TALKER_ID_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    BDS_TALKER_ID_FIELD_NUMBER: _ClassVar[int]
    RESERVED1_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    filter: int
    nmea_version: int
    num_sv: int
    flags: int
    gnss_to_filter: int
    sv_numbering: int
    main_talker_id: int
    gsv_talker_id: int
    version: int
    bds_talker_id: _containers.RepeatedScalarFieldContainer[int]
    reserved1: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., filter: _Optional[int] = ..., nmea_version: _Optional[int] = ..., num_sv: _Optional[int] = ..., flags: _Optional[int] = ..., gnss_to_filter: _Optional[int] = ..., sv_numbering: _Optional[int] = ..., main_talker_id: _Optional[int] = ..., gsv_talker_id: _Optional[int] = ..., version: _Optional[int] = ..., bds_talker_id: _Optional[_Iterable[int]] = ..., reserved1: _Optional[_Iterable[int]] = ...) -> None: ...
