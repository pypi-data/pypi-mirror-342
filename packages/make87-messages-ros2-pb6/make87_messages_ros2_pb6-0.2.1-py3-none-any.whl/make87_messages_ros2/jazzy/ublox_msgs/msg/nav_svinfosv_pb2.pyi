from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class NavSVINFOSV(_message.Message):
    __slots__ = ("chn", "svid", "flags", "quality", "cno", "elev", "azim", "pr_res")
    CHN_FIELD_NUMBER: _ClassVar[int]
    SVID_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    QUALITY_FIELD_NUMBER: _ClassVar[int]
    CNO_FIELD_NUMBER: _ClassVar[int]
    ELEV_FIELD_NUMBER: _ClassVar[int]
    AZIM_FIELD_NUMBER: _ClassVar[int]
    PR_RES_FIELD_NUMBER: _ClassVar[int]
    chn: int
    svid: int
    flags: int
    quality: int
    cno: int
    elev: int
    azim: int
    pr_res: int
    def __init__(self, chn: _Optional[int] = ..., svid: _Optional[int] = ..., flags: _Optional[int] = ..., quality: _Optional[int] = ..., cno: _Optional[int] = ..., elev: _Optional[int] = ..., azim: _Optional[int] = ..., pr_res: _Optional[int] = ...) -> None: ...
