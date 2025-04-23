from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class NavPOSLLH(_message.Message):
    __slots__ = ("i_tow", "lon", "lat", "height", "h_msl", "h_acc", "v_acc")
    I_TOW_FIELD_NUMBER: _ClassVar[int]
    LON_FIELD_NUMBER: _ClassVar[int]
    LAT_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    H_MSL_FIELD_NUMBER: _ClassVar[int]
    H_ACC_FIELD_NUMBER: _ClassVar[int]
    V_ACC_FIELD_NUMBER: _ClassVar[int]
    i_tow: int
    lon: int
    lat: int
    height: int
    h_msl: int
    h_acc: int
    v_acc: int
    def __init__(self, i_tow: _Optional[int] = ..., lon: _Optional[int] = ..., lat: _Optional[int] = ..., height: _Optional[int] = ..., h_msl: _Optional[int] = ..., h_acc: _Optional[int] = ..., v_acc: _Optional[int] = ...) -> None: ...
