from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import float32_multi_array_pb2 as _float32_multi_array_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from make87_messages_ros2.humble.std_msgs.msg import int32_pb2 as _int32_pb2
from make87_messages_ros2.humble.std_msgs.msg import string_pb2 as _string_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DetectionInfo(_message.Message):
    __slots__ = ("header", "ros2_header", "ids", "widths", "heights", "file_paths", "inliers", "outliers", "homographies")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    IDS_FIELD_NUMBER: _ClassVar[int]
    WIDTHS_FIELD_NUMBER: _ClassVar[int]
    HEIGHTS_FIELD_NUMBER: _ClassVar[int]
    FILE_PATHS_FIELD_NUMBER: _ClassVar[int]
    INLIERS_FIELD_NUMBER: _ClassVar[int]
    OUTLIERS_FIELD_NUMBER: _ClassVar[int]
    HOMOGRAPHIES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    ids: _containers.RepeatedCompositeFieldContainer[_int32_pb2.Int32]
    widths: _containers.RepeatedCompositeFieldContainer[_int32_pb2.Int32]
    heights: _containers.RepeatedCompositeFieldContainer[_int32_pb2.Int32]
    file_paths: _containers.RepeatedCompositeFieldContainer[_string_pb2.String]
    inliers: _containers.RepeatedCompositeFieldContainer[_int32_pb2.Int32]
    outliers: _containers.RepeatedCompositeFieldContainer[_int32_pb2.Int32]
    homographies: _containers.RepeatedCompositeFieldContainer[_float32_multi_array_pb2.Float32MultiArray]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., ids: _Optional[_Iterable[_Union[_int32_pb2.Int32, _Mapping]]] = ..., widths: _Optional[_Iterable[_Union[_int32_pb2.Int32, _Mapping]]] = ..., heights: _Optional[_Iterable[_Union[_int32_pb2.Int32, _Mapping]]] = ..., file_paths: _Optional[_Iterable[_Union[_string_pb2.String, _Mapping]]] = ..., inliers: _Optional[_Iterable[_Union[_int32_pb2.Int32, _Mapping]]] = ..., outliers: _Optional[_Iterable[_Union[_int32_pb2.Int32, _Mapping]]] = ..., homographies: _Optional[_Iterable[_Union[_float32_multi_array_pb2.Float32MultiArray, _Mapping]]] = ...) -> None: ...
