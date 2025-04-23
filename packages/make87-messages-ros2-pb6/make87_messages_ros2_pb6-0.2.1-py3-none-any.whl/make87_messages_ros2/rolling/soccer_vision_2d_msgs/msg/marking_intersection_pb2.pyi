from make87_messages_ros2.rolling.soccer_vision_attribute_msgs.msg import confidence_pb2 as _confidence_pb2
from make87_messages_ros2.rolling.vision_msgs.msg import point2_d_pb2 as _point2_d_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MarkingIntersection(_message.Message):
    __slots__ = ("center", "num_rays", "heading_rays", "confidence")
    CENTER_FIELD_NUMBER: _ClassVar[int]
    NUM_RAYS_FIELD_NUMBER: _ClassVar[int]
    HEADING_RAYS_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    center: _point2_d_pb2.Point2D
    num_rays: int
    heading_rays: _containers.RepeatedScalarFieldContainer[float]
    confidence: _confidence_pb2.Confidence
    def __init__(self, center: _Optional[_Union[_point2_d_pb2.Point2D, _Mapping]] = ..., num_rays: _Optional[int] = ..., heading_rays: _Optional[_Iterable[float]] = ..., confidence: _Optional[_Union[_confidence_pb2.Confidence, _Mapping]] = ...) -> None: ...
