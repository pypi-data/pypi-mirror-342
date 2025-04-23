from make87_messages_ros2.jazzy.sick_safevisionary_interfaces.msg import field_information_pb2 as _field_information_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FieldInformationArray(_message.Message):
    __slots__ = ("header", "fields")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    fields: _containers.RepeatedCompositeFieldContainer[_field_information_pb2.FieldInformation]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., fields: _Optional[_Iterable[_Union[_field_information_pb2.FieldInformation, _Mapping]]] = ...) -> None: ...
