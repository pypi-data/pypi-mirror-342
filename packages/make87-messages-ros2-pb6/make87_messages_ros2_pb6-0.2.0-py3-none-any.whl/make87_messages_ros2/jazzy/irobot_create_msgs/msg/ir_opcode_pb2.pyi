from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IrOpcode(_message.Message):
    __slots__ = ("header", "opcode", "sensor")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    OPCODE_FIELD_NUMBER: _ClassVar[int]
    SENSOR_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    opcode: int
    sensor: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., opcode: _Optional[int] = ..., sensor: _Optional[int] = ...) -> None: ...
