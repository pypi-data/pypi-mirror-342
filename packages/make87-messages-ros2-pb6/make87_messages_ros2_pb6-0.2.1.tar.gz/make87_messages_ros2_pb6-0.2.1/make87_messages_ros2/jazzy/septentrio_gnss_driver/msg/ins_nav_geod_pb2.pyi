from make87_messages_ros2.jazzy.septentrio_gnss_driver.msg import block_header_pb2 as _block_header_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class INSNavGeod(_message.Message):
    __slots__ = ("header", "block_header", "gnss_mode", "error", "info", "gnss_age", "latitude", "longitude", "height", "undulation", "accuracy", "latency", "datum", "sb_list", "latitude_std_dev", "longitude_std_dev", "height_std_dev", "latitude_longitude_cov", "latitude_height_cov", "longitude_height_cov", "heading", "pitch", "roll", "heading_std_dev", "pitch_std_dev", "roll_std_dev", "heading_pitch_cov", "heading_roll_cov", "pitch_roll_cov", "ve", "vn", "vu", "ve_std_dev", "vn_std_dev", "vu_std_dev", "ve_vn_cov", "ve_vu_cov", "vn_vu_cov")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BLOCK_HEADER_FIELD_NUMBER: _ClassVar[int]
    GNSS_MODE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    GNSS_AGE_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    UNDULATION_FIELD_NUMBER: _ClassVar[int]
    ACCURACY_FIELD_NUMBER: _ClassVar[int]
    LATENCY_FIELD_NUMBER: _ClassVar[int]
    DATUM_FIELD_NUMBER: _ClassVar[int]
    SB_LIST_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_STD_DEV_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_STD_DEV_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_STD_DEV_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_LONGITUDE_COV_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_HEIGHT_COV_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_HEIGHT_COV_FIELD_NUMBER: _ClassVar[int]
    HEADING_FIELD_NUMBER: _ClassVar[int]
    PITCH_FIELD_NUMBER: _ClassVar[int]
    ROLL_FIELD_NUMBER: _ClassVar[int]
    HEADING_STD_DEV_FIELD_NUMBER: _ClassVar[int]
    PITCH_STD_DEV_FIELD_NUMBER: _ClassVar[int]
    ROLL_STD_DEV_FIELD_NUMBER: _ClassVar[int]
    HEADING_PITCH_COV_FIELD_NUMBER: _ClassVar[int]
    HEADING_ROLL_COV_FIELD_NUMBER: _ClassVar[int]
    PITCH_ROLL_COV_FIELD_NUMBER: _ClassVar[int]
    VE_FIELD_NUMBER: _ClassVar[int]
    VN_FIELD_NUMBER: _ClassVar[int]
    VU_FIELD_NUMBER: _ClassVar[int]
    VE_STD_DEV_FIELD_NUMBER: _ClassVar[int]
    VN_STD_DEV_FIELD_NUMBER: _ClassVar[int]
    VU_STD_DEV_FIELD_NUMBER: _ClassVar[int]
    VE_VN_COV_FIELD_NUMBER: _ClassVar[int]
    VE_VU_COV_FIELD_NUMBER: _ClassVar[int]
    VN_VU_COV_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    block_header: _block_header_pb2.BlockHeader
    gnss_mode: int
    error: int
    info: int
    gnss_age: int
    latitude: float
    longitude: float
    height: float
    undulation: float
    accuracy: int
    latency: int
    datum: int
    sb_list: int
    latitude_std_dev: float
    longitude_std_dev: float
    height_std_dev: float
    latitude_longitude_cov: float
    latitude_height_cov: float
    longitude_height_cov: float
    heading: float
    pitch: float
    roll: float
    heading_std_dev: float
    pitch_std_dev: float
    roll_std_dev: float
    heading_pitch_cov: float
    heading_roll_cov: float
    pitch_roll_cov: float
    ve: float
    vn: float
    vu: float
    ve_std_dev: float
    vn_std_dev: float
    vu_std_dev: float
    ve_vn_cov: float
    ve_vu_cov: float
    vn_vu_cov: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., block_header: _Optional[_Union[_block_header_pb2.BlockHeader, _Mapping]] = ..., gnss_mode: _Optional[int] = ..., error: _Optional[int] = ..., info: _Optional[int] = ..., gnss_age: _Optional[int] = ..., latitude: _Optional[float] = ..., longitude: _Optional[float] = ..., height: _Optional[float] = ..., undulation: _Optional[float] = ..., accuracy: _Optional[int] = ..., latency: _Optional[int] = ..., datum: _Optional[int] = ..., sb_list: _Optional[int] = ..., latitude_std_dev: _Optional[float] = ..., longitude_std_dev: _Optional[float] = ..., height_std_dev: _Optional[float] = ..., latitude_longitude_cov: _Optional[float] = ..., latitude_height_cov: _Optional[float] = ..., longitude_height_cov: _Optional[float] = ..., heading: _Optional[float] = ..., pitch: _Optional[float] = ..., roll: _Optional[float] = ..., heading_std_dev: _Optional[float] = ..., pitch_std_dev: _Optional[float] = ..., roll_std_dev: _Optional[float] = ..., heading_pitch_cov: _Optional[float] = ..., heading_roll_cov: _Optional[float] = ..., pitch_roll_cov: _Optional[float] = ..., ve: _Optional[float] = ..., vn: _Optional[float] = ..., vu: _Optional[float] = ..., ve_std_dev: _Optional[float] = ..., vn_std_dev: _Optional[float] = ..., vu_std_dev: _Optional[float] = ..., ve_vn_cov: _Optional[float] = ..., ve_vu_cov: _Optional[float] = ..., vn_vu_cov: _Optional[float] = ...) -> None: ...
