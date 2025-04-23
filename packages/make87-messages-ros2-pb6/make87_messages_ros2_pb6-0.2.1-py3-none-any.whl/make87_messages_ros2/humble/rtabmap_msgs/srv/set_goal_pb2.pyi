from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_pb2 as _pose_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetGoalRequest(_message.Message):
    __slots__ = ("header", "node_id", "node_label", "frame_id")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    NODE_LABEL_FIELD_NUMBER: _ClassVar[int]
    FRAME_ID_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    node_id: int
    node_label: str
    frame_id: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., node_id: _Optional[int] = ..., node_label: _Optional[str] = ..., frame_id: _Optional[str] = ...) -> None: ...

class SetGoalResponse(_message.Message):
    __slots__ = ("header", "path_ids", "path_poses", "planning_time")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PATH_IDS_FIELD_NUMBER: _ClassVar[int]
    PATH_POSES_FIELD_NUMBER: _ClassVar[int]
    PLANNING_TIME_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    path_ids: _containers.RepeatedScalarFieldContainer[int]
    path_poses: _containers.RepeatedCompositeFieldContainer[_pose_pb2.Pose]
    planning_time: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., path_ids: _Optional[_Iterable[int]] = ..., path_poses: _Optional[_Iterable[_Union[_pose_pb2.Pose, _Mapping]]] = ..., planning_time: _Optional[float] = ...) -> None: ...
