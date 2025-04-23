from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GimbalManagerSetRoiRequest(_message.Message):
    __slots__ = ("header", "mode", "gimbal_device_id", "latitude", "longitude", "altitude", "pitch_offset", "roll_offset", "yaw_offset", "sysid")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    GIMBAL_DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_FIELD_NUMBER: _ClassVar[int]
    PITCH_OFFSET_FIELD_NUMBER: _ClassVar[int]
    ROLL_OFFSET_FIELD_NUMBER: _ClassVar[int]
    YAW_OFFSET_FIELD_NUMBER: _ClassVar[int]
    SYSID_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    mode: int
    gimbal_device_id: int
    latitude: float
    longitude: float
    altitude: float
    pitch_offset: float
    roll_offset: float
    yaw_offset: float
    sysid: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., mode: _Optional[int] = ..., gimbal_device_id: _Optional[int] = ..., latitude: _Optional[float] = ..., longitude: _Optional[float] = ..., altitude: _Optional[float] = ..., pitch_offset: _Optional[float] = ..., roll_offset: _Optional[float] = ..., yaw_offset: _Optional[float] = ..., sysid: _Optional[int] = ...) -> None: ...

class GimbalManagerSetRoiResponse(_message.Message):
    __slots__ = ("header", "success", "result")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    result: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., result: _Optional[int] = ...) -> None: ...
