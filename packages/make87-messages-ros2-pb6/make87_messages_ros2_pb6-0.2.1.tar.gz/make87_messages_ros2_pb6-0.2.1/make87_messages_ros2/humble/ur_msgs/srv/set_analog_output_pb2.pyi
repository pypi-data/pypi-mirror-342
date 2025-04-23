from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.ur_msgs.msg import analog_pb2 as _analog_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetAnalogOutputRequest(_message.Message):
    __slots__ = ("header", "data")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    data: _analog_pb2.Analog
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., data: _Optional[_Union[_analog_pb2.Analog, _Mapping]] = ...) -> None: ...

class SetAnalogOutputResponse(_message.Message):
    __slots__ = ("header", "success")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ...) -> None: ...
