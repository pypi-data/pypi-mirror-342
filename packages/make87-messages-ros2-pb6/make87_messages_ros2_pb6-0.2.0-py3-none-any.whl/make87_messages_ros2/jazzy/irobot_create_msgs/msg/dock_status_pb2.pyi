from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DockStatus(_message.Message):
    __slots__ = ("header", "dock_visible", "is_docked")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DOCK_VISIBLE_FIELD_NUMBER: _ClassVar[int]
    IS_DOCKED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    dock_visible: bool
    is_docked: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., dock_visible: bool = ..., is_docked: bool = ...) -> None: ...
