from make87_messages_ros2.rolling.rmf_reservation_msgs.msg import ticket_pb2 as _ticket_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ReleaseRequest(_message.Message):
    __slots__ = ("ticket", "location")
    TICKET_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    ticket: _ticket_pb2.Ticket
    location: str
    def __init__(self, ticket: _Optional[_Union[_ticket_pb2.Ticket, _Mapping]] = ..., location: _Optional[str] = ...) -> None: ...
