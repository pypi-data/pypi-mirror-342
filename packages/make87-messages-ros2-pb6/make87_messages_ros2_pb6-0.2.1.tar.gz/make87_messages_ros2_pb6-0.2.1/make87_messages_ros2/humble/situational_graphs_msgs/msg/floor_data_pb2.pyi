from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FloorData(_message.Message):
    __slots__ = ("header", "ros2_header", "id", "floor_center", "keyframe_ids", "state")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    FLOOR_CENTER_FIELD_NUMBER: _ClassVar[int]
    KEYFRAME_IDS_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    id: int
    floor_center: _pose_pb2.Pose
    keyframe_ids: _containers.RepeatedScalarFieldContainer[int]
    state: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., id: _Optional[int] = ..., floor_center: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., keyframe_ids: _Optional[_Iterable[int]] = ..., state: _Optional[int] = ...) -> None: ...
