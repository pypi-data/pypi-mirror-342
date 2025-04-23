from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rmf_traffic_msgs.msg import participant_description_pb2 as _participant_description_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Participant(_message.Message):
    __slots__ = ("header", "id", "description")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    id: int
    description: _participant_description_pb2.ParticipantDescription
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., id: _Optional[int] = ..., description: _Optional[_Union[_participant_description_pb2.ParticipantDescription, _Mapping]] = ...) -> None: ...
