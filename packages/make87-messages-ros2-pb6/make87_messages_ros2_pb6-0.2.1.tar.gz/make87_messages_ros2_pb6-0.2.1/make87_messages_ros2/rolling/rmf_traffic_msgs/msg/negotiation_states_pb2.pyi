from make87_messages_ros2.rolling.rmf_traffic_msgs.msg import negotiation_state_pb2 as _negotiation_state_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NegotiationStates(_message.Message):
    __slots__ = ("negotiations",)
    NEGOTIATIONS_FIELD_NUMBER: _ClassVar[int]
    negotiations: _containers.RepeatedCompositeFieldContainer[_negotiation_state_pb2.NegotiationState]
    def __init__(self, negotiations: _Optional[_Iterable[_Union[_negotiation_state_pb2.NegotiationState, _Mapping]]] = ...) -> None: ...
