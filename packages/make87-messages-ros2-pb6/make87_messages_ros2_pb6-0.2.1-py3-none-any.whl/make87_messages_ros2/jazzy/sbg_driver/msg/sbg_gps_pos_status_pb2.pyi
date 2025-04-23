from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SbgGpsPosStatus(_message.Message):
    __slots__ = ("status", "type", "ifm", "spoofing", "osnma", "gps_l1_used", "gps_l2_used", "gps_l5_used", "glo_l1_used", "glo_l2_used", "glo_l3_used", "gal_e1_used", "gal_e5a_used", "gal_e5b_used", "gal_e5alt_used", "gal_e6_used", "bds_b1_used", "bds_b2_used", "bds_b3_used", "qzss_l1_used", "qzss_l2_used", "qzss_l5_used")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    IFM_FIELD_NUMBER: _ClassVar[int]
    SPOOFING_FIELD_NUMBER: _ClassVar[int]
    OSNMA_FIELD_NUMBER: _ClassVar[int]
    GPS_L1_USED_FIELD_NUMBER: _ClassVar[int]
    GPS_L2_USED_FIELD_NUMBER: _ClassVar[int]
    GPS_L5_USED_FIELD_NUMBER: _ClassVar[int]
    GLO_L1_USED_FIELD_NUMBER: _ClassVar[int]
    GLO_L2_USED_FIELD_NUMBER: _ClassVar[int]
    GLO_L3_USED_FIELD_NUMBER: _ClassVar[int]
    GAL_E1_USED_FIELD_NUMBER: _ClassVar[int]
    GAL_E5A_USED_FIELD_NUMBER: _ClassVar[int]
    GAL_E5B_USED_FIELD_NUMBER: _ClassVar[int]
    GAL_E5ALT_USED_FIELD_NUMBER: _ClassVar[int]
    GAL_E6_USED_FIELD_NUMBER: _ClassVar[int]
    BDS_B1_USED_FIELD_NUMBER: _ClassVar[int]
    BDS_B2_USED_FIELD_NUMBER: _ClassVar[int]
    BDS_B3_USED_FIELD_NUMBER: _ClassVar[int]
    QZSS_L1_USED_FIELD_NUMBER: _ClassVar[int]
    QZSS_L2_USED_FIELD_NUMBER: _ClassVar[int]
    QZSS_L5_USED_FIELD_NUMBER: _ClassVar[int]
    status: int
    type: int
    ifm: int
    spoofing: int
    osnma: int
    gps_l1_used: bool
    gps_l2_used: bool
    gps_l5_used: bool
    glo_l1_used: bool
    glo_l2_used: bool
    glo_l3_used: bool
    gal_e1_used: bool
    gal_e5a_used: bool
    gal_e5b_used: bool
    gal_e5alt_used: bool
    gal_e6_used: bool
    bds_b1_used: bool
    bds_b2_used: bool
    bds_b3_used: bool
    qzss_l1_used: bool
    qzss_l2_used: bool
    qzss_l5_used: bool
    def __init__(self, status: _Optional[int] = ..., type: _Optional[int] = ..., ifm: _Optional[int] = ..., spoofing: _Optional[int] = ..., osnma: _Optional[int] = ..., gps_l1_used: bool = ..., gps_l2_used: bool = ..., gps_l5_used: bool = ..., glo_l1_used: bool = ..., glo_l2_used: bool = ..., glo_l3_used: bool = ..., gal_e1_used: bool = ..., gal_e5a_used: bool = ..., gal_e5b_used: bool = ..., gal_e5alt_used: bool = ..., gal_e6_used: bool = ..., bds_b1_used: bool = ..., bds_b2_used: bool = ..., bds_b3_used: bool = ..., qzss_l1_used: bool = ..., qzss_l2_used: bool = ..., qzss_l5_used: bool = ...) -> None: ...
