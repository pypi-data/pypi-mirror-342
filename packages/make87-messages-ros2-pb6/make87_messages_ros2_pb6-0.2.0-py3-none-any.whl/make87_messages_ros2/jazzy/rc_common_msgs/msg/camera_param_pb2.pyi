from make87_messages_ros2.jazzy.rc_common_msgs.msg import key_value_pb2 as _key_value_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CameraParam(_message.Message):
    __slots__ = ("header", "is_color_camera", "exposure_time", "gain", "line_status_all", "line_source", "extra_data")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    IS_COLOR_CAMERA_FIELD_NUMBER: _ClassVar[int]
    EXPOSURE_TIME_FIELD_NUMBER: _ClassVar[int]
    GAIN_FIELD_NUMBER: _ClassVar[int]
    LINE_STATUS_ALL_FIELD_NUMBER: _ClassVar[int]
    LINE_SOURCE_FIELD_NUMBER: _ClassVar[int]
    EXTRA_DATA_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    is_color_camera: bool
    exposure_time: float
    gain: float
    line_status_all: int
    line_source: _containers.RepeatedCompositeFieldContainer[_key_value_pb2.KeyValue]
    extra_data: _containers.RepeatedCompositeFieldContainer[_key_value_pb2.KeyValue]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., is_color_camera: bool = ..., exposure_time: _Optional[float] = ..., gain: _Optional[float] = ..., line_status_all: _Optional[int] = ..., line_source: _Optional[_Iterable[_Union[_key_value_pb2.KeyValue, _Mapping]]] = ..., extra_data: _Optional[_Iterable[_Union[_key_value_pb2.KeyValue, _Mapping]]] = ...) -> None: ...
