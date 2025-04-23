from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HilActuatorControls(_message.Message):
    __slots__ = ("header", "controls", "mode", "flags")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CONTROLS_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    controls: _containers.RepeatedScalarFieldContainer[float]
    mode: int
    flags: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., controls: _Optional[_Iterable[float]] = ..., mode: _Optional[int] = ..., flags: _Optional[int] = ...) -> None: ...
