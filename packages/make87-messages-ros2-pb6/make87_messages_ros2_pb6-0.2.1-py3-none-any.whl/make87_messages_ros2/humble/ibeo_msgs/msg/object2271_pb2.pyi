from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.ibeo_msgs.msg import tracked_properties_pb2 as _tracked_properties_pb2
from make87_messages_ros2.humble.ibeo_msgs.msg import untracked_properties_pb2 as _untracked_properties_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Object2271(_message.Message):
    __slots__ = ("header", "id", "tracked_properties_available", "untracked_properties_available", "tracked_properties", "untracked_properties")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    TRACKED_PROPERTIES_AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    UNTRACKED_PROPERTIES_AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    TRACKED_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    UNTRACKED_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    id: int
    tracked_properties_available: bool
    untracked_properties_available: bool
    tracked_properties: _tracked_properties_pb2.TrackedProperties
    untracked_properties: _untracked_properties_pb2.UntrackedProperties
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., id: _Optional[int] = ..., tracked_properties_available: bool = ..., untracked_properties_available: bool = ..., tracked_properties: _Optional[_Union[_tracked_properties_pb2.TrackedProperties, _Mapping]] = ..., untracked_properties: _Optional[_Union[_untracked_properties_pb2.UntrackedProperties, _Mapping]] = ...) -> None: ...
