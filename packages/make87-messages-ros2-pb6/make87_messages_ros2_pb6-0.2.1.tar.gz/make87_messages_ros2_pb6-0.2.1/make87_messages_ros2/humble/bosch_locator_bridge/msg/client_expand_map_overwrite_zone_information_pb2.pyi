from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import point32_pb2 as _point32_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ClientExpandMapOverwriteZoneInformation(_message.Message):
    __slots__ = ("header", "id", "name", "type", "polygon")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    POLYGON_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    id: int
    name: str
    type: int
    polygon: _containers.RepeatedCompositeFieldContainer[_point32_pb2.Point32]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., id: _Optional[int] = ..., name: _Optional[str] = ..., type: _Optional[int] = ..., polygon: _Optional[_Iterable[_Union[_point32_pb2.Point32, _Mapping]]] = ...) -> None: ...
