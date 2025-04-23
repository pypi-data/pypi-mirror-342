from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geographic_msgs.msg import key_value_pb2 as _key_value_pb2
from make87_messages_ros2.humble.unique_identifier_msgs.msg import uuid_pb2 as _uuid_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RouteSegment(_message.Message):
    __slots__ = ("header", "id", "start", "end", "props")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    PROPS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    id: _uuid_pb2.UUID
    start: _uuid_pb2.UUID
    end: _uuid_pb2.UUID
    props: _containers.RepeatedCompositeFieldContainer[_key_value_pb2.KeyValue]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., id: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., start: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., end: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., props: _Optional[_Iterable[_Union[_key_value_pb2.KeyValue, _Mapping]]] = ...) -> None: ...
