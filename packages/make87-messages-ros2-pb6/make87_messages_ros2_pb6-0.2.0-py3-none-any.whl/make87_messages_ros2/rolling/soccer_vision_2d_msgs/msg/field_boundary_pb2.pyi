from make87_messages_ros2.rolling.soccer_vision_attribute_msgs.msg import confidence_pb2 as _confidence_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from make87_messages_ros2.rolling.vision_msgs.msg import point2_d_pb2 as _point2_d_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FieldBoundary(_message.Message):
    __slots__ = ("header", "points", "confidence")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    points: _containers.RepeatedCompositeFieldContainer[_point2_d_pb2.Point2D]
    confidence: _confidence_pb2.Confidence
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., points: _Optional[_Iterable[_Union[_point2_d_pb2.Point2D, _Mapping]]] = ..., confidence: _Optional[_Union[_confidence_pb2.Confidence, _Mapping]] = ...) -> None: ...
