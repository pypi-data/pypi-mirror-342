from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rosbridge_test_msgs.msg import test_float32_bounded_array_pb2 as _test_float32_bounded_array_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TestNestedBoundedArray(_message.Message):
    __slots__ = ("header", "data")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    data: _test_float32_bounded_array_pb2.TestFloat32BoundedArray
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., data: _Optional[_Union[_test_float32_bounded_array_pb2.TestFloat32BoundedArray, _Mapping]] = ...) -> None: ...
