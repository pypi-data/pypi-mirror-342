from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PerceptionCameraParameters(_message.Message):
    __slots__ = ("header", "ros2_header", "stereo_cameras_direction", "left_intrinsics", "right_intrinsics", "rotation_left_in_right", "translation_left_in_right")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    STEREO_CAMERAS_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    LEFT_INTRINSICS_FIELD_NUMBER: _ClassVar[int]
    RIGHT_INTRINSICS_FIELD_NUMBER: _ClassVar[int]
    ROTATION_LEFT_IN_RIGHT_FIELD_NUMBER: _ClassVar[int]
    TRANSLATION_LEFT_IN_RIGHT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    stereo_cameras_direction: int
    left_intrinsics: _containers.RepeatedScalarFieldContainer[float]
    right_intrinsics: _containers.RepeatedScalarFieldContainer[float]
    rotation_left_in_right: _containers.RepeatedScalarFieldContainer[float]
    translation_left_in_right: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., stereo_cameras_direction: _Optional[int] = ..., left_intrinsics: _Optional[_Iterable[float]] = ..., right_intrinsics: _Optional[_Iterable[float]] = ..., rotation_left_in_right: _Optional[_Iterable[float]] = ..., translation_left_in_right: _Optional[_Iterable[float]] = ...) -> None: ...
