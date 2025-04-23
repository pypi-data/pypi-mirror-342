from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class NavSVIN(_message.Message):
    __slots__ = ("version", "reserved0", "i_tow", "dur", "mean_x", "mean_y", "mean_z", "mean_xhp", "mean_yhp", "mean_zhp", "reserved1", "mean_acc", "obs", "valid", "active", "reserved3")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    RESERVED0_FIELD_NUMBER: _ClassVar[int]
    I_TOW_FIELD_NUMBER: _ClassVar[int]
    DUR_FIELD_NUMBER: _ClassVar[int]
    MEAN_X_FIELD_NUMBER: _ClassVar[int]
    MEAN_Y_FIELD_NUMBER: _ClassVar[int]
    MEAN_Z_FIELD_NUMBER: _ClassVar[int]
    MEAN_XHP_FIELD_NUMBER: _ClassVar[int]
    MEAN_YHP_FIELD_NUMBER: _ClassVar[int]
    MEAN_ZHP_FIELD_NUMBER: _ClassVar[int]
    RESERVED1_FIELD_NUMBER: _ClassVar[int]
    MEAN_ACC_FIELD_NUMBER: _ClassVar[int]
    OBS_FIELD_NUMBER: _ClassVar[int]
    VALID_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    RESERVED3_FIELD_NUMBER: _ClassVar[int]
    version: int
    reserved0: _containers.RepeatedScalarFieldContainer[int]
    i_tow: int
    dur: int
    mean_x: int
    mean_y: int
    mean_z: int
    mean_xhp: int
    mean_yhp: int
    mean_zhp: int
    reserved1: int
    mean_acc: int
    obs: int
    valid: int
    active: int
    reserved3: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, version: _Optional[int] = ..., reserved0: _Optional[_Iterable[int]] = ..., i_tow: _Optional[int] = ..., dur: _Optional[int] = ..., mean_x: _Optional[int] = ..., mean_y: _Optional[int] = ..., mean_z: _Optional[int] = ..., mean_xhp: _Optional[int] = ..., mean_yhp: _Optional[int] = ..., mean_zhp: _Optional[int] = ..., reserved1: _Optional[int] = ..., mean_acc: _Optional[int] = ..., obs: _Optional[int] = ..., valid: _Optional[int] = ..., active: _Optional[int] = ..., reserved3: _Optional[_Iterable[int]] = ...) -> None: ...
