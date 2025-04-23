from make87_messages_ros2.rolling.rmf_reservation_msgs.msg import flexible_time_reservation_alt_pb2 as _flexible_time_reservation_alt_pb2
from make87_messages_ros2.rolling.rmf_reservation_msgs.msg import request_header_pb2 as _request_header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FlexibleTimeRequest(_message.Message):
    __slots__ = ("header", "alternatives")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ALTERNATIVES_FIELD_NUMBER: _ClassVar[int]
    header: _request_header_pb2.RequestHeader
    alternatives: _containers.RepeatedCompositeFieldContainer[_flexible_time_reservation_alt_pb2.FlexibleTimeReservationAlt]
    def __init__(self, header: _Optional[_Union[_request_header_pb2.RequestHeader, _Mapping]] = ..., alternatives: _Optional[_Iterable[_Union[_flexible_time_reservation_alt_pb2.FlexibleTimeReservationAlt, _Mapping]]] = ...) -> None: ...
