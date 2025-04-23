from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class WorkcellRequest(_message.Message):
    __slots__ = ("header", "time", "request_guid", "target_guid")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    REQUEST_GUID_FIELD_NUMBER: _ClassVar[int]
    TARGET_GUID_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    time: _time_pb2.Time
    request_guid: str
    target_guid: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., request_guid: _Optional[str] = ..., target_guid: _Optional[str] = ...) -> None: ...
