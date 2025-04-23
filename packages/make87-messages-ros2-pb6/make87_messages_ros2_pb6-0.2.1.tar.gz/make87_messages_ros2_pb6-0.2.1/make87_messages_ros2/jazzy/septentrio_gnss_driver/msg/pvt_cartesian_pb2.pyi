from make87_messages_ros2.jazzy.septentrio_gnss_driver.msg import block_header_pb2 as _block_header_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PVTCartesian(_message.Message):
    __slots__ = ("header", "block_header", "mode", "error", "x", "y", "z", "undulation", "vx", "vy", "vz", "cog", "rx_clk_bias", "rx_clk_drift", "time_system", "datum", "nr_sv", "wa_corr_info", "reference_id", "mean_corr_age", "signal_info", "alert_flag", "nr_bases", "ppp_info", "latency", "h_accuracy", "v_accuracy", "misc")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BLOCK_HEADER_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    UNDULATION_FIELD_NUMBER: _ClassVar[int]
    VX_FIELD_NUMBER: _ClassVar[int]
    VY_FIELD_NUMBER: _ClassVar[int]
    VZ_FIELD_NUMBER: _ClassVar[int]
    COG_FIELD_NUMBER: _ClassVar[int]
    RX_CLK_BIAS_FIELD_NUMBER: _ClassVar[int]
    RX_CLK_DRIFT_FIELD_NUMBER: _ClassVar[int]
    TIME_SYSTEM_FIELD_NUMBER: _ClassVar[int]
    DATUM_FIELD_NUMBER: _ClassVar[int]
    NR_SV_FIELD_NUMBER: _ClassVar[int]
    WA_CORR_INFO_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_ID_FIELD_NUMBER: _ClassVar[int]
    MEAN_CORR_AGE_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_INFO_FIELD_NUMBER: _ClassVar[int]
    ALERT_FLAG_FIELD_NUMBER: _ClassVar[int]
    NR_BASES_FIELD_NUMBER: _ClassVar[int]
    PPP_INFO_FIELD_NUMBER: _ClassVar[int]
    LATENCY_FIELD_NUMBER: _ClassVar[int]
    H_ACCURACY_FIELD_NUMBER: _ClassVar[int]
    V_ACCURACY_FIELD_NUMBER: _ClassVar[int]
    MISC_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    block_header: _block_header_pb2.BlockHeader
    mode: int
    error: int
    x: float
    y: float
    z: float
    undulation: float
    vx: float
    vy: float
    vz: float
    cog: float
    rx_clk_bias: float
    rx_clk_drift: float
    time_system: int
    datum: int
    nr_sv: int
    wa_corr_info: int
    reference_id: int
    mean_corr_age: int
    signal_info: int
    alert_flag: int
    nr_bases: int
    ppp_info: int
    latency: int
    h_accuracy: int
    v_accuracy: int
    misc: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., block_header: _Optional[_Union[_block_header_pb2.BlockHeader, _Mapping]] = ..., mode: _Optional[int] = ..., error: _Optional[int] = ..., x: _Optional[float] = ..., y: _Optional[float] = ..., z: _Optional[float] = ..., undulation: _Optional[float] = ..., vx: _Optional[float] = ..., vy: _Optional[float] = ..., vz: _Optional[float] = ..., cog: _Optional[float] = ..., rx_clk_bias: _Optional[float] = ..., rx_clk_drift: _Optional[float] = ..., time_system: _Optional[int] = ..., datum: _Optional[int] = ..., nr_sv: _Optional[int] = ..., wa_corr_info: _Optional[int] = ..., reference_id: _Optional[int] = ..., mean_corr_age: _Optional[int] = ..., signal_info: _Optional[int] = ..., alert_flag: _Optional[int] = ..., nr_bases: _Optional[int] = ..., ppp_info: _Optional[int] = ..., latency: _Optional[int] = ..., h_accuracy: _Optional[int] = ..., v_accuracy: _Optional[int] = ..., misc: _Optional[int] = ...) -> None: ...
