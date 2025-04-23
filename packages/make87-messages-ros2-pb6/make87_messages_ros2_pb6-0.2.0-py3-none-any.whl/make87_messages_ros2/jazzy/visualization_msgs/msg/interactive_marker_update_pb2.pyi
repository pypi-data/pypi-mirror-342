from make87_messages_ros2.jazzy.visualization_msgs.msg import interactive_marker_pb2 as _interactive_marker_pb2
from make87_messages_ros2.jazzy.visualization_msgs.msg import interactive_marker_pose_pb2 as _interactive_marker_pose_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class InteractiveMarkerUpdate(_message.Message):
    __slots__ = ("server_id", "seq_num", "type", "markers", "poses", "erases")
    SERVER_ID_FIELD_NUMBER: _ClassVar[int]
    SEQ_NUM_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    MARKERS_FIELD_NUMBER: _ClassVar[int]
    POSES_FIELD_NUMBER: _ClassVar[int]
    ERASES_FIELD_NUMBER: _ClassVar[int]
    server_id: str
    seq_num: int
    type: int
    markers: _containers.RepeatedCompositeFieldContainer[_interactive_marker_pb2.InteractiveMarker]
    poses: _containers.RepeatedCompositeFieldContainer[_interactive_marker_pose_pb2.InteractiveMarkerPose]
    erases: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, server_id: _Optional[str] = ..., seq_num: _Optional[int] = ..., type: _Optional[int] = ..., markers: _Optional[_Iterable[_Union[_interactive_marker_pb2.InteractiveMarker, _Mapping]]] = ..., poses: _Optional[_Iterable[_Union[_interactive_marker_pose_pb2.InteractiveMarkerPose, _Mapping]]] = ..., erases: _Optional[_Iterable[str]] = ...) -> None: ...
