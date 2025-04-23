from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CfgNMEA7(_message.Message):
    __slots__ = ("filter", "nmea_version", "num_sv", "flags", "gnss_to_filter", "sv_numbering", "main_talker_id", "gsv_talker_id", "reserved")
    FILTER_FIELD_NUMBER: _ClassVar[int]
    NMEA_VERSION_FIELD_NUMBER: _ClassVar[int]
    NUM_SV_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    GNSS_TO_FILTER_FIELD_NUMBER: _ClassVar[int]
    SV_NUMBERING_FIELD_NUMBER: _ClassVar[int]
    MAIN_TALKER_ID_FIELD_NUMBER: _ClassVar[int]
    GSV_TALKER_ID_FIELD_NUMBER: _ClassVar[int]
    RESERVED_FIELD_NUMBER: _ClassVar[int]
    filter: int
    nmea_version: int
    num_sv: int
    flags: int
    gnss_to_filter: int
    sv_numbering: int
    main_talker_id: int
    gsv_talker_id: int
    reserved: int
    def __init__(self, filter: _Optional[int] = ..., nmea_version: _Optional[int] = ..., num_sv: _Optional[int] = ..., flags: _Optional[int] = ..., gnss_to_filter: _Optional[int] = ..., sv_numbering: _Optional[int] = ..., main_talker_id: _Optional[int] = ..., gsv_talker_id: _Optional[int] = ..., reserved: _Optional[int] = ...) -> None: ...
