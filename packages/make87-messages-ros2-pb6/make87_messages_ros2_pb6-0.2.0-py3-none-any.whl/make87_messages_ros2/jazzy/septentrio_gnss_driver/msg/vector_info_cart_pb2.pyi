from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class VectorInfoCart(_message.Message):
    __slots__ = ("nr_sv", "error", "mode", "misc", "delta_x", "delta_y", "delta_z", "delta_vx", "delta_vy", "delta_vz", "azimuth", "elevation", "reference_id", "corr_age", "signal_info")
    NR_SV_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    MISC_FIELD_NUMBER: _ClassVar[int]
    DELTA_X_FIELD_NUMBER: _ClassVar[int]
    DELTA_Y_FIELD_NUMBER: _ClassVar[int]
    DELTA_Z_FIELD_NUMBER: _ClassVar[int]
    DELTA_VX_FIELD_NUMBER: _ClassVar[int]
    DELTA_VY_FIELD_NUMBER: _ClassVar[int]
    DELTA_VZ_FIELD_NUMBER: _ClassVar[int]
    AZIMUTH_FIELD_NUMBER: _ClassVar[int]
    ELEVATION_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_ID_FIELD_NUMBER: _ClassVar[int]
    CORR_AGE_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_INFO_FIELD_NUMBER: _ClassVar[int]
    nr_sv: int
    error: int
    mode: int
    misc: int
    delta_x: float
    delta_y: float
    delta_z: float
    delta_vx: float
    delta_vy: float
    delta_vz: float
    azimuth: int
    elevation: int
    reference_id: int
    corr_age: int
    signal_info: int
    def __init__(self, nr_sv: _Optional[int] = ..., error: _Optional[int] = ..., mode: _Optional[int] = ..., misc: _Optional[int] = ..., delta_x: _Optional[float] = ..., delta_y: _Optional[float] = ..., delta_z: _Optional[float] = ..., delta_vx: _Optional[float] = ..., delta_vy: _Optional[float] = ..., delta_vz: _Optional[float] = ..., azimuth: _Optional[int] = ..., elevation: _Optional[int] = ..., reference_id: _Optional[int] = ..., corr_age: _Optional[int] = ..., signal_info: _Optional[int] = ...) -> None: ...
