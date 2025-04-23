from make87_messages_ros2.jazzy.rmf_traffic_msgs.msg import negotiation_key_pb2 as _negotiation_key_pb2
from make87_messages_ros2.jazzy.rmf_traffic_msgs.msg import route_pb2 as _route_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NegotiationTreeNode(_message.Message):
    __slots__ = ("parent", "key", "rejected", "itinerary")
    PARENT_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    REJECTED_FIELD_NUMBER: _ClassVar[int]
    ITINERARY_FIELD_NUMBER: _ClassVar[int]
    parent: int
    key: _negotiation_key_pb2.NegotiationKey
    rejected: bool
    itinerary: _containers.RepeatedCompositeFieldContainer[_route_pb2.Route]
    def __init__(self, parent: _Optional[int] = ..., key: _Optional[_Union[_negotiation_key_pb2.NegotiationKey, _Mapping]] = ..., rejected: bool = ..., itinerary: _Optional[_Iterable[_Union[_route_pb2.Route, _Mapping]]] = ...) -> None: ...
