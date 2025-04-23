from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CfgGNSSBlock(_message.Message):
    __slots__ = ("gnss_id", "res_trk_ch", "max_trk_ch", "reserved1", "flags")
    GNSS_ID_FIELD_NUMBER: _ClassVar[int]
    RES_TRK_CH_FIELD_NUMBER: _ClassVar[int]
    MAX_TRK_CH_FIELD_NUMBER: _ClassVar[int]
    RESERVED1_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    gnss_id: int
    res_trk_ch: int
    max_trk_ch: int
    reserved1: int
    flags: int
    def __init__(self, gnss_id: _Optional[int] = ..., res_trk_ch: _Optional[int] = ..., max_trk_ch: _Optional[int] = ..., reserved1: _Optional[int] = ..., flags: _Optional[int] = ...) -> None: ...
