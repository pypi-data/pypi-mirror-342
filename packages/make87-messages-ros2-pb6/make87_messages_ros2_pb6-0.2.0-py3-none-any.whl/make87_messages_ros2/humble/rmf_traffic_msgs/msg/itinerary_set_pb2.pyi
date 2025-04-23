from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rmf_traffic_msgs.msg import route_pb2 as _route_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ItinerarySet(_message.Message):
    __slots__ = ("header", "participant", "plan", "itinerary", "storage_base", "itinerary_version")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PARTICIPANT_FIELD_NUMBER: _ClassVar[int]
    PLAN_FIELD_NUMBER: _ClassVar[int]
    ITINERARY_FIELD_NUMBER: _ClassVar[int]
    STORAGE_BASE_FIELD_NUMBER: _ClassVar[int]
    ITINERARY_VERSION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    participant: int
    plan: int
    itinerary: _containers.RepeatedCompositeFieldContainer[_route_pb2.Route]
    storage_base: int
    itinerary_version: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., participant: _Optional[int] = ..., plan: _Optional[int] = ..., itinerary: _Optional[_Iterable[_Union[_route_pb2.Route, _Mapping]]] = ..., storage_base: _Optional[int] = ..., itinerary_version: _Optional[int] = ...) -> None: ...
