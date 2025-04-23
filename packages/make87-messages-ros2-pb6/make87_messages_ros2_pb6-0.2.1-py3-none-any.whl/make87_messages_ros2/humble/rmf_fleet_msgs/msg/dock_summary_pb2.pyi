from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rmf_fleet_msgs.msg import dock_pb2 as _dock_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DockSummary(_message.Message):
    __slots__ = ("header", "docks")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DOCKS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    docks: _containers.RepeatedCompositeFieldContainer[_dock_pb2.Dock]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., docks: _Optional[_Iterable[_Union[_dock_pb2.Dock, _Mapping]]] = ...) -> None: ...
