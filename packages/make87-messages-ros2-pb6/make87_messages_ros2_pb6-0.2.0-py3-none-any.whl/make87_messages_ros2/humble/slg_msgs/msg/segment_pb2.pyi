from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import point_pb2 as _point_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Segment(_message.Message):
    __slots__ = ("header", "id", "label", "angular_distance", "last_point_prior_segment", "first_point_next_segment", "points")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    ANGULAR_DISTANCE_FIELD_NUMBER: _ClassVar[int]
    LAST_POINT_PRIOR_SEGMENT_FIELD_NUMBER: _ClassVar[int]
    FIRST_POINT_NEXT_SEGMENT_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    id: int
    label: int
    angular_distance: float
    last_point_prior_segment: _point_pb2.Point
    first_point_next_segment: _point_pb2.Point
    points: _containers.RepeatedCompositeFieldContainer[_point_pb2.Point]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., id: _Optional[int] = ..., label: _Optional[int] = ..., angular_distance: _Optional[float] = ..., last_point_prior_segment: _Optional[_Union[_point_pb2.Point, _Mapping]] = ..., first_point_next_segment: _Optional[_Union[_point_pb2.Point, _Mapping]] = ..., points: _Optional[_Iterable[_Union[_point_pb2.Point, _Mapping]]] = ...) -> None: ...
