from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GimbalManagerPitchyawRequest(_message.Message):
    __slots__ = ("header", "pitch", "yaw", "pitch_rate", "yaw_rate", "flags", "gimbal_device_id")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PITCH_FIELD_NUMBER: _ClassVar[int]
    YAW_FIELD_NUMBER: _ClassVar[int]
    PITCH_RATE_FIELD_NUMBER: _ClassVar[int]
    YAW_RATE_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    GIMBAL_DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    pitch: float
    yaw: float
    pitch_rate: float
    yaw_rate: float
    flags: int
    gimbal_device_id: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., pitch: _Optional[float] = ..., yaw: _Optional[float] = ..., pitch_rate: _Optional[float] = ..., yaw_rate: _Optional[float] = ..., flags: _Optional[int] = ..., gimbal_device_id: _Optional[int] = ...) -> None: ...

class GimbalManagerPitchyawResponse(_message.Message):
    __slots__ = ("header", "success", "result")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    result: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., result: _Optional[int] = ...) -> None: ...
