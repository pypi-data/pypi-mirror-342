from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rmf_traffic_msgs.msg import negotiation_key_pb2 as _negotiation_key_pb2
from make87_messages_ros2.humble.rmf_traffic_msgs.msg import route_pb2 as _route_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NegotiationProposal(_message.Message):
    __slots__ = ("header", "conflict_version", "proposal_version", "for_participant", "to_accommodate", "plan_id", "itinerary")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CONFLICT_VERSION_FIELD_NUMBER: _ClassVar[int]
    PROPOSAL_VERSION_FIELD_NUMBER: _ClassVar[int]
    FOR_PARTICIPANT_FIELD_NUMBER: _ClassVar[int]
    TO_ACCOMMODATE_FIELD_NUMBER: _ClassVar[int]
    PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    ITINERARY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    conflict_version: int
    proposal_version: int
    for_participant: int
    to_accommodate: _containers.RepeatedCompositeFieldContainer[_negotiation_key_pb2.NegotiationKey]
    plan_id: int
    itinerary: _containers.RepeatedCompositeFieldContainer[_route_pb2.Route]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., conflict_version: _Optional[int] = ..., proposal_version: _Optional[int] = ..., for_participant: _Optional[int] = ..., to_accommodate: _Optional[_Iterable[_Union[_negotiation_key_pb2.NegotiationKey, _Mapping]]] = ..., plan_id: _Optional[int] = ..., itinerary: _Optional[_Iterable[_Union[_route_pb2.Route, _Mapping]]] = ...) -> None: ...
