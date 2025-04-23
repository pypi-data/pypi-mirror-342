from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UBXNavHPPosLLH(_message.Message):
    __slots__ = ("header", "version", "invalid_lon", "invalid_lat", "invalid_height", "invalid_hmsl", "invalid_lon_hp", "invalid_lat_hp", "invalid_height_hp", "invalid_hmsl_hp", "itow", "lon", "lat", "height", "hmsl", "lon_hp", "lat_hp", "height_hp", "hmsl_hp", "h_acc", "v_acc")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    INVALID_LON_FIELD_NUMBER: _ClassVar[int]
    INVALID_LAT_FIELD_NUMBER: _ClassVar[int]
    INVALID_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    INVALID_HMSL_FIELD_NUMBER: _ClassVar[int]
    INVALID_LON_HP_FIELD_NUMBER: _ClassVar[int]
    INVALID_LAT_HP_FIELD_NUMBER: _ClassVar[int]
    INVALID_HEIGHT_HP_FIELD_NUMBER: _ClassVar[int]
    INVALID_HMSL_HP_FIELD_NUMBER: _ClassVar[int]
    ITOW_FIELD_NUMBER: _ClassVar[int]
    LON_FIELD_NUMBER: _ClassVar[int]
    LAT_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    HMSL_FIELD_NUMBER: _ClassVar[int]
    LON_HP_FIELD_NUMBER: _ClassVar[int]
    LAT_HP_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_HP_FIELD_NUMBER: _ClassVar[int]
    HMSL_HP_FIELD_NUMBER: _ClassVar[int]
    H_ACC_FIELD_NUMBER: _ClassVar[int]
    V_ACC_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    version: int
    invalid_lon: bool
    invalid_lat: bool
    invalid_height: bool
    invalid_hmsl: bool
    invalid_lon_hp: bool
    invalid_lat_hp: bool
    invalid_height_hp: bool
    invalid_hmsl_hp: bool
    itow: int
    lon: int
    lat: int
    height: int
    hmsl: int
    lon_hp: int
    lat_hp: int
    height_hp: int
    hmsl_hp: int
    h_acc: int
    v_acc: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., version: _Optional[int] = ..., invalid_lon: bool = ..., invalid_lat: bool = ..., invalid_height: bool = ..., invalid_hmsl: bool = ..., invalid_lon_hp: bool = ..., invalid_lat_hp: bool = ..., invalid_height_hp: bool = ..., invalid_hmsl_hp: bool = ..., itow: _Optional[int] = ..., lon: _Optional[int] = ..., lat: _Optional[int] = ..., height: _Optional[int] = ..., hmsl: _Optional[int] = ..., lon_hp: _Optional[int] = ..., lat_hp: _Optional[int] = ..., height_hp: _Optional[int] = ..., hmsl_hp: _Optional[int] = ..., h_acc: _Optional[int] = ..., v_acc: _Optional[int] = ...) -> None: ...
