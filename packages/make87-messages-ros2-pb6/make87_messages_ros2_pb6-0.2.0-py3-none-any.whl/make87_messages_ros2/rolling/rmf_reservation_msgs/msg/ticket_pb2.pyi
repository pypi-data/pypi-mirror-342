from make87_messages_ros2.rolling.rmf_reservation_msgs.msg import request_header_pb2 as _request_header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Ticket(_message.Message):
    __slots__ = ("header", "ticket_id")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TICKET_ID_FIELD_NUMBER: _ClassVar[int]
    header: _request_header_pb2.RequestHeader
    ticket_id: int
    def __init__(self, header: _Optional[_Union[_request_header_pb2.RequestHeader, _Mapping]] = ..., ticket_id: _Optional[int] = ...) -> None: ...
