from make87_messages_ros2.rolling.septentrio_gnss_driver.msg import block_header_pb2 as _block_header_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class INSNavCart(_message.Message):
    __slots__ = ("header", "block_header", "gnss_mode", "error", "info", "gnss_age", "x", "y", "z", "accuracy", "latency", "datum", "sb_list", "x_std_dev", "y_std_dev", "z_std_dev", "xy_cov", "xz_cov", "yz_cov", "heading", "pitch", "roll", "heading_std_dev", "pitch_std_dev", "roll_std_dev", "heading_pitch_cov", "heading_roll_cov", "pitch_roll_cov", "vx", "vy", "vz", "vx_std_dev", "vy_std_dev", "vz_std_dev", "vx_vy_cov", "vx_vz_cov", "vy_vz_cov")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BLOCK_HEADER_FIELD_NUMBER: _ClassVar[int]
    GNSS_MODE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    GNSS_AGE_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    ACCURACY_FIELD_NUMBER: _ClassVar[int]
    LATENCY_FIELD_NUMBER: _ClassVar[int]
    DATUM_FIELD_NUMBER: _ClassVar[int]
    SB_LIST_FIELD_NUMBER: _ClassVar[int]
    X_STD_DEV_FIELD_NUMBER: _ClassVar[int]
    Y_STD_DEV_FIELD_NUMBER: _ClassVar[int]
    Z_STD_DEV_FIELD_NUMBER: _ClassVar[int]
    XY_COV_FIELD_NUMBER: _ClassVar[int]
    XZ_COV_FIELD_NUMBER: _ClassVar[int]
    YZ_COV_FIELD_NUMBER: _ClassVar[int]
    HEADING_FIELD_NUMBER: _ClassVar[int]
    PITCH_FIELD_NUMBER: _ClassVar[int]
    ROLL_FIELD_NUMBER: _ClassVar[int]
    HEADING_STD_DEV_FIELD_NUMBER: _ClassVar[int]
    PITCH_STD_DEV_FIELD_NUMBER: _ClassVar[int]
    ROLL_STD_DEV_FIELD_NUMBER: _ClassVar[int]
    HEADING_PITCH_COV_FIELD_NUMBER: _ClassVar[int]
    HEADING_ROLL_COV_FIELD_NUMBER: _ClassVar[int]
    PITCH_ROLL_COV_FIELD_NUMBER: _ClassVar[int]
    VX_FIELD_NUMBER: _ClassVar[int]
    VY_FIELD_NUMBER: _ClassVar[int]
    VZ_FIELD_NUMBER: _ClassVar[int]
    VX_STD_DEV_FIELD_NUMBER: _ClassVar[int]
    VY_STD_DEV_FIELD_NUMBER: _ClassVar[int]
    VZ_STD_DEV_FIELD_NUMBER: _ClassVar[int]
    VX_VY_COV_FIELD_NUMBER: _ClassVar[int]
    VX_VZ_COV_FIELD_NUMBER: _ClassVar[int]
    VY_VZ_COV_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    block_header: _block_header_pb2.BlockHeader
    gnss_mode: int
    error: int
    info: int
    gnss_age: int
    x: float
    y: float
    z: float
    accuracy: int
    latency: int
    datum: int
    sb_list: int
    x_std_dev: float
    y_std_dev: float
    z_std_dev: float
    xy_cov: float
    xz_cov: float
    yz_cov: float
    heading: float
    pitch: float
    roll: float
    heading_std_dev: float
    pitch_std_dev: float
    roll_std_dev: float
    heading_pitch_cov: float
    heading_roll_cov: float
    pitch_roll_cov: float
    vx: float
    vy: float
    vz: float
    vx_std_dev: float
    vy_std_dev: float
    vz_std_dev: float
    vx_vy_cov: float
    vx_vz_cov: float
    vy_vz_cov: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., block_header: _Optional[_Union[_block_header_pb2.BlockHeader, _Mapping]] = ..., gnss_mode: _Optional[int] = ..., error: _Optional[int] = ..., info: _Optional[int] = ..., gnss_age: _Optional[int] = ..., x: _Optional[float] = ..., y: _Optional[float] = ..., z: _Optional[float] = ..., accuracy: _Optional[int] = ..., latency: _Optional[int] = ..., datum: _Optional[int] = ..., sb_list: _Optional[int] = ..., x_std_dev: _Optional[float] = ..., y_std_dev: _Optional[float] = ..., z_std_dev: _Optional[float] = ..., xy_cov: _Optional[float] = ..., xz_cov: _Optional[float] = ..., yz_cov: _Optional[float] = ..., heading: _Optional[float] = ..., pitch: _Optional[float] = ..., roll: _Optional[float] = ..., heading_std_dev: _Optional[float] = ..., pitch_std_dev: _Optional[float] = ..., roll_std_dev: _Optional[float] = ..., heading_pitch_cov: _Optional[float] = ..., heading_roll_cov: _Optional[float] = ..., pitch_roll_cov: _Optional[float] = ..., vx: _Optional[float] = ..., vy: _Optional[float] = ..., vz: _Optional[float] = ..., vx_std_dev: _Optional[float] = ..., vy_std_dev: _Optional[float] = ..., vz_std_dev: _Optional[float] = ..., vx_vy_cov: _Optional[float] = ..., vx_vz_cov: _Optional[float] = ..., vy_vz_cov: _Optional[float] = ...) -> None: ...
