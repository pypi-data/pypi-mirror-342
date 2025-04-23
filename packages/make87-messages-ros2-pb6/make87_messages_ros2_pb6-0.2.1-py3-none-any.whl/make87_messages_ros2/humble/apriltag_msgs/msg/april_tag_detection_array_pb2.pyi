from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.apriltag_msgs.msg import april_tag_detection_pb2 as _april_tag_detection_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AprilTagDetectionArray(_message.Message):
    __slots__ = ("header", "ros2_header", "detections")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    DETECTIONS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    detections: _containers.RepeatedCompositeFieldContainer[_april_tag_detection_pb2.AprilTagDetection]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., detections: _Optional[_Iterable[_Union[_april_tag_detection_pb2.AprilTagDetection, _Mapping]]] = ...) -> None: ...
