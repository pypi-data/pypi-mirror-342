from make87_messages_ros2.rolling.soccer_vision_attribute_msgs.msg import confidence_pb2 as _confidence_pb2
from make87_messages_ros2.rolling.vision_msgs.msg import point2_d_pb2 as _point2_d_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MarkingSegment(_message.Message):
    __slots__ = ("start", "end", "confidence")
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    start: _point2_d_pb2.Point2D
    end: _point2_d_pb2.Point2D
    confidence: _confidence_pb2.Confidence
    def __init__(self, start: _Optional[_Union[_point2_d_pb2.Point2D, _Mapping]] = ..., end: _Optional[_Union[_point2_d_pb2.Point2D, _Mapping]] = ..., confidence: _Optional[_Union[_confidence_pb2.Confidence, _Mapping]] = ...) -> None: ...
