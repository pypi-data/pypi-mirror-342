from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CfgNAV5(_message.Message):
    __slots__ = ("mask", "dyn_model", "fix_mode", "fixed_alt", "fixed_alt_var", "min_elev", "dr_limit", "p_dop", "t_dop", "p_acc", "t_acc", "static_hold_thresh", "dgnss_time_out", "cno_thresh_num_svs", "cno_thresh", "reserved1", "static_hold_max_dist", "utc_standard", "reserved2")
    MASK_FIELD_NUMBER: _ClassVar[int]
    DYN_MODEL_FIELD_NUMBER: _ClassVar[int]
    FIX_MODE_FIELD_NUMBER: _ClassVar[int]
    FIXED_ALT_FIELD_NUMBER: _ClassVar[int]
    FIXED_ALT_VAR_FIELD_NUMBER: _ClassVar[int]
    MIN_ELEV_FIELD_NUMBER: _ClassVar[int]
    DR_LIMIT_FIELD_NUMBER: _ClassVar[int]
    P_DOP_FIELD_NUMBER: _ClassVar[int]
    T_DOP_FIELD_NUMBER: _ClassVar[int]
    P_ACC_FIELD_NUMBER: _ClassVar[int]
    T_ACC_FIELD_NUMBER: _ClassVar[int]
    STATIC_HOLD_THRESH_FIELD_NUMBER: _ClassVar[int]
    DGNSS_TIME_OUT_FIELD_NUMBER: _ClassVar[int]
    CNO_THRESH_NUM_SVS_FIELD_NUMBER: _ClassVar[int]
    CNO_THRESH_FIELD_NUMBER: _ClassVar[int]
    RESERVED1_FIELD_NUMBER: _ClassVar[int]
    STATIC_HOLD_MAX_DIST_FIELD_NUMBER: _ClassVar[int]
    UTC_STANDARD_FIELD_NUMBER: _ClassVar[int]
    RESERVED2_FIELD_NUMBER: _ClassVar[int]
    mask: int
    dyn_model: int
    fix_mode: int
    fixed_alt: int
    fixed_alt_var: int
    min_elev: int
    dr_limit: int
    p_dop: int
    t_dop: int
    p_acc: int
    t_acc: int
    static_hold_thresh: int
    dgnss_time_out: int
    cno_thresh_num_svs: int
    cno_thresh: int
    reserved1: _containers.RepeatedScalarFieldContainer[int]
    static_hold_max_dist: int
    utc_standard: int
    reserved2: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, mask: _Optional[int] = ..., dyn_model: _Optional[int] = ..., fix_mode: _Optional[int] = ..., fixed_alt: _Optional[int] = ..., fixed_alt_var: _Optional[int] = ..., min_elev: _Optional[int] = ..., dr_limit: _Optional[int] = ..., p_dop: _Optional[int] = ..., t_dop: _Optional[int] = ..., p_acc: _Optional[int] = ..., t_acc: _Optional[int] = ..., static_hold_thresh: _Optional[int] = ..., dgnss_time_out: _Optional[int] = ..., cno_thresh_num_svs: _Optional[int] = ..., cno_thresh: _Optional[int] = ..., reserved1: _Optional[_Iterable[int]] = ..., static_hold_max_dist: _Optional[int] = ..., utc_standard: _Optional[int] = ..., reserved2: _Optional[_Iterable[int]] = ...) -> None: ...
