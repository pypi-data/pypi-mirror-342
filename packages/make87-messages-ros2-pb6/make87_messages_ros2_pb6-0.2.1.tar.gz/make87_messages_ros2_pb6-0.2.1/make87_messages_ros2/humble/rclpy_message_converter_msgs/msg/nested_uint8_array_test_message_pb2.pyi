from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rclpy_message_converter_msgs.msg import uint8_array_test_message_pb2 as _uint8_array_test_message_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NestedUint8ArrayTestMessage(_message.Message):
    __slots__ = ("header", "arrays")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ARRAYS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    arrays: _containers.RepeatedCompositeFieldContainer[_uint8_array_test_message_pb2.Uint8ArrayTestMessage]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., arrays: _Optional[_Iterable[_Union[_uint8_array_test_message_pb2.Uint8ArrayTestMessage, _Mapping]]] = ...) -> None: ...
