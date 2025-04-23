from make87_messages_ros2.rolling.motion_capture_tracking_interfaces.msg import named_pose_pb2 as _named_pose_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NamedPoseArray(_message.Message):
    __slots__ = ("header", "poses")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    POSES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    poses: _containers.RepeatedCompositeFieldContainer[_named_pose_pb2.NamedPose]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., poses: _Optional[_Iterable[_Union[_named_pose_pb2.NamedPose, _Mapping]]] = ...) -> None: ...
