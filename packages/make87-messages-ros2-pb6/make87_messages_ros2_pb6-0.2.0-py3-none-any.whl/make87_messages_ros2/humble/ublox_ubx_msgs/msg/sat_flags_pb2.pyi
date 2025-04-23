from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SatFlags(_message.Message):
    __slots__ = ("header", "quality_ind", "sv_used", "health", "diff_corr", "smoothed", "orbit_source", "eph_avail", "alm_avail", "ano_avail", "aop_avail", "sbas_corr_used", "rtcm_corr_used", "slas_corr_used", "spartn_corr_used", "pr_corr_used", "cr_corr_used", "do_corr_used", "clas_corr_used")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    QUALITY_IND_FIELD_NUMBER: _ClassVar[int]
    SV_USED_FIELD_NUMBER: _ClassVar[int]
    HEALTH_FIELD_NUMBER: _ClassVar[int]
    DIFF_CORR_FIELD_NUMBER: _ClassVar[int]
    SMOOTHED_FIELD_NUMBER: _ClassVar[int]
    ORBIT_SOURCE_FIELD_NUMBER: _ClassVar[int]
    EPH_AVAIL_FIELD_NUMBER: _ClassVar[int]
    ALM_AVAIL_FIELD_NUMBER: _ClassVar[int]
    ANO_AVAIL_FIELD_NUMBER: _ClassVar[int]
    AOP_AVAIL_FIELD_NUMBER: _ClassVar[int]
    SBAS_CORR_USED_FIELD_NUMBER: _ClassVar[int]
    RTCM_CORR_USED_FIELD_NUMBER: _ClassVar[int]
    SLAS_CORR_USED_FIELD_NUMBER: _ClassVar[int]
    SPARTN_CORR_USED_FIELD_NUMBER: _ClassVar[int]
    PR_CORR_USED_FIELD_NUMBER: _ClassVar[int]
    CR_CORR_USED_FIELD_NUMBER: _ClassVar[int]
    DO_CORR_USED_FIELD_NUMBER: _ClassVar[int]
    CLAS_CORR_USED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    quality_ind: int
    sv_used: bool
    health: int
    diff_corr: bool
    smoothed: bool
    orbit_source: int
    eph_avail: bool
    alm_avail: bool
    ano_avail: bool
    aop_avail: bool
    sbas_corr_used: bool
    rtcm_corr_used: bool
    slas_corr_used: bool
    spartn_corr_used: bool
    pr_corr_used: bool
    cr_corr_used: bool
    do_corr_used: bool
    clas_corr_used: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., quality_ind: _Optional[int] = ..., sv_used: bool = ..., health: _Optional[int] = ..., diff_corr: bool = ..., smoothed: bool = ..., orbit_source: _Optional[int] = ..., eph_avail: bool = ..., alm_avail: bool = ..., ano_avail: bool = ..., aop_avail: bool = ..., sbas_corr_used: bool = ..., rtcm_corr_used: bool = ..., slas_corr_used: bool = ..., spartn_corr_used: bool = ..., pr_corr_used: bool = ..., cr_corr_used: bool = ..., do_corr_used: bool = ..., clas_corr_used: bool = ...) -> None: ...
