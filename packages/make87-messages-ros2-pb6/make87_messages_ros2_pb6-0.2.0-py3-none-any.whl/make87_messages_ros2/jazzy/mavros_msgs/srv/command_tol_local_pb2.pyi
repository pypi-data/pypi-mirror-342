from make87_messages_ros2.jazzy.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CommandTOLLocalRequest(_message.Message):
    __slots__ = ("min_pitch", "offset", "rate", "yaw", "position")
    MIN_PITCH_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    RATE_FIELD_NUMBER: _ClassVar[int]
    YAW_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    min_pitch: float
    offset: float
    rate: float
    yaw: float
    position: _vector3_pb2.Vector3
    def __init__(self, min_pitch: _Optional[float] = ..., offset: _Optional[float] = ..., rate: _Optional[float] = ..., yaw: _Optional[float] = ..., position: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ...) -> None: ...

class CommandTOLLocalResponse(_message.Message):
    __slots__ = ("success", "result")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    success: bool
    result: int
    def __init__(self, success: bool = ..., result: _Optional[int] = ...) -> None: ...
