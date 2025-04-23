from make87_messages_ros2.jazzy.depthai_ros_msgs.msg import spatial_detection_pb2 as _spatial_detection_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SpatialDetectionArray(_message.Message):
    __slots__ = ("header", "detections")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DETECTIONS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    detections: _containers.RepeatedCompositeFieldContainer[_spatial_detection_pb2.SpatialDetection]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., detections: _Optional[_Iterable[_Union[_spatial_detection_pb2.SpatialDetection, _Mapping]]] = ...) -> None: ...
