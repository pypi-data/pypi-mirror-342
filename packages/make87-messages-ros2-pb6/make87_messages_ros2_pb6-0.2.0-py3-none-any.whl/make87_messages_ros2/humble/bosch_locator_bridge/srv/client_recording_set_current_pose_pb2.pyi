from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose2_d_pb2 as _pose2_d_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ClientRecordingSetCurrentPoseRequest(_message.Message):
    __slots__ = ("header", "pose")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    pose: _pose2_d_pb2.Pose2D
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., pose: _Optional[_Union[_pose2_d_pb2.Pose2D, _Mapping]] = ...) -> None: ...

class ClientRecordingSetCurrentPoseResponse(_message.Message):
    __slots__ = ("header",)
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...
