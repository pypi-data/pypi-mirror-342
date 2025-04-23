from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rclpy_message_converter_msgs.msg import nested_uint8_array_test_message_pb2 as _nested_uint8_array_test_message_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NestedUint8ArrayTestServiceRequest(_message.Message):
    __slots__ = ("header", "input")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    INPUT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    input: _nested_uint8_array_test_message_pb2.NestedUint8ArrayTestMessage
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., input: _Optional[_Union[_nested_uint8_array_test_message_pb2.NestedUint8ArrayTestMessage, _Mapping]] = ...) -> None: ...

class NestedUint8ArrayTestServiceResponse(_message.Message):
    __slots__ = ("header", "output")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    output: _nested_uint8_array_test_message_pb2.NestedUint8ArrayTestMessage
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., output: _Optional[_Union[_nested_uint8_array_test_message_pb2.NestedUint8ArrayTestMessage, _Mapping]] = ...) -> None: ...
