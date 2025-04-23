from make87_messages_ros2.jazzy.sick_scan_xd.msg import lf_erec_field_msg_pb2 as _lf_erec_field_msg_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LFErecMsg(_message.Message):
    __slots__ = ("header", "fields_number", "fields")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FIELDS_NUMBER_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    fields_number: int
    fields: _containers.RepeatedCompositeFieldContainer[_lf_erec_field_msg_pb2.LFErecFieldMsg]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., fields_number: _Optional[int] = ..., fields: _Optional[_Iterable[_Union[_lf_erec_field_msg_pb2.LFErecFieldMsg, _Mapping]]] = ...) -> None: ...
