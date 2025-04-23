from make87_messages_ros2.rolling.soccer_vision_attribute_msgs.msg import confidence_pb2 as _confidence_pb2
from make87_messages_ros2.rolling.vision_msgs.msg import bounding_box3_d_pb2 as _bounding_box3_d_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Obstacle(_message.Message):
    __slots__ = ("bb", "confidence")
    BB_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    bb: _bounding_box3_d_pb2.BoundingBox3D
    confidence: _confidence_pb2.Confidence
    def __init__(self, bb: _Optional[_Union[_bounding_box3_d_pb2.BoundingBox3D, _Mapping]] = ..., confidence: _Optional[_Union[_confidence_pb2.Confidence, _Mapping]] = ...) -> None: ...
