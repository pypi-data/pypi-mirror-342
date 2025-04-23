from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_pb2 as _pose_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetHandEyeCalibrationPoseRequest(_message.Message):
    __slots__ = ("header", "slot", "pose")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SLOT_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    slot: int
    pose: _pose_pb2.Pose
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., slot: _Optional[int] = ..., pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ...) -> None: ...

class SetHandEyeCalibrationPoseResponse(_message.Message):
    __slots__ = ("header", "success", "status", "message")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    status: int
    message: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., status: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...
