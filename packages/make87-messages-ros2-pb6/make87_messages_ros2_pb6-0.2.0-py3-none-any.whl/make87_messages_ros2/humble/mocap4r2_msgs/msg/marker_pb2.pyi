from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import point_pb2 as _point_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Marker(_message.Message):
    __slots__ = ("header", "id_type", "marker_index", "marker_name", "translation")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ID_TYPE_FIELD_NUMBER: _ClassVar[int]
    MARKER_INDEX_FIELD_NUMBER: _ClassVar[int]
    MARKER_NAME_FIELD_NUMBER: _ClassVar[int]
    TRANSLATION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    id_type: int
    marker_index: int
    marker_name: str
    translation: _point_pb2.Point
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., id_type: _Optional[int] = ..., marker_index: _Optional[int] = ..., marker_name: _Optional[str] = ..., translation: _Optional[_Union[_point_pb2.Point, _Mapping]] = ...) -> None: ...
