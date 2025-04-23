from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geographic_msgs.msg import geographic_map_changes_pb2 as _geographic_map_changes_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UpdateGeographicMapRequest(_message.Message):
    __slots__ = ("header", "updates")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    UPDATES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    updates: _geographic_map_changes_pb2.GeographicMapChanges
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., updates: _Optional[_Union[_geographic_map_changes_pb2.GeographicMapChanges, _Mapping]] = ...) -> None: ...

class UpdateGeographicMapResponse(_message.Message):
    __slots__ = ("header", "success", "status")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    status: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., status: _Optional[str] = ...) -> None: ...
