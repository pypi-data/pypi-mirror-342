from make87_messages_ros2.jazzy.geometry_msgs.msg import point_pb2 as _point_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LaneBoundary(_message.Message):
    __slots__ = ("style", "color", "line")
    STYLE_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    LINE_FIELD_NUMBER: _ClassVar[int]
    style: int
    color: int
    line: _containers.RepeatedCompositeFieldContainer[_point_pb2.Point]
    def __init__(self, style: _Optional[int] = ..., color: _Optional[int] = ..., line: _Optional[_Iterable[_Union[_point_pb2.Point, _Mapping]]] = ...) -> None: ...
