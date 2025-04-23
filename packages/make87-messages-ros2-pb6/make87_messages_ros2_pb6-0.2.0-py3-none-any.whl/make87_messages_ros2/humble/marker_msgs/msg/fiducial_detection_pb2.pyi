from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.marker_msgs.msg import fiducial_pb2 as _fiducial_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FiducialDetection(_message.Message):
    __slots__ = ("header", "ros2_header", "camera_d", "camera_k", "type", "fiducial")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    CAMERA_D_FIELD_NUMBER: _ClassVar[int]
    CAMERA_K_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    FIDUCIAL_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    camera_d: _containers.RepeatedScalarFieldContainer[float]
    camera_k: _containers.RepeatedScalarFieldContainer[float]
    type: str
    fiducial: _containers.RepeatedCompositeFieldContainer[_fiducial_pb2.Fiducial]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., camera_d: _Optional[_Iterable[float]] = ..., camera_k: _Optional[_Iterable[float]] = ..., type: _Optional[str] = ..., fiducial: _Optional[_Iterable[_Union[_fiducial_pb2.Fiducial, _Mapping]]] = ...) -> None: ...
