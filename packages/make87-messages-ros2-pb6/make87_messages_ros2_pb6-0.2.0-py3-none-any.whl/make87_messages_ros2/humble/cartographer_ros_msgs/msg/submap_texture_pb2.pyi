from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_pb2 as _pose_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SubmapTexture(_message.Message):
    __slots__ = ("header", "cells", "width", "height", "resolution", "slice_pose")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CELLS_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    RESOLUTION_FIELD_NUMBER: _ClassVar[int]
    SLICE_POSE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    cells: _containers.RepeatedScalarFieldContainer[int]
    width: int
    height: int
    resolution: float
    slice_pose: _pose_pb2.Pose
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., cells: _Optional[_Iterable[int]] = ..., width: _Optional[int] = ..., height: _Optional[int] = ..., resolution: _Optional[float] = ..., slice_pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ...) -> None: ...
