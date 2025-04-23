from make87_messages_ros2.jazzy.geometry_msgs.msg import pose_pb2 as _pose_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetHandEyeCalibrationRequest(_message.Message):
    __slots__ = ("pose", "robot_mounted")
    POSE_FIELD_NUMBER: _ClassVar[int]
    ROBOT_MOUNTED_FIELD_NUMBER: _ClassVar[int]
    pose: _pose_pb2.Pose
    robot_mounted: bool
    def __init__(self, pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., robot_mounted: bool = ...) -> None: ...

class SetHandEyeCalibrationResponse(_message.Message):
    __slots__ = ("success", "status", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    status: int
    message: str
    def __init__(self, success: bool = ..., status: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...
