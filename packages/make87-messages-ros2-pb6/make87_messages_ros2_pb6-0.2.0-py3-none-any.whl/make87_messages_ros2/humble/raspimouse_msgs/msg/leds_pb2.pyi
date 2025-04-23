from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Leds(_message.Message):
    __slots__ = ("header", "led0", "led1", "led2", "led3")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LED0_FIELD_NUMBER: _ClassVar[int]
    LED1_FIELD_NUMBER: _ClassVar[int]
    LED2_FIELD_NUMBER: _ClassVar[int]
    LED3_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    led0: bool
    led1: bool
    led2: bool
    led3: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., led0: bool = ..., led1: bool = ..., led2: bool = ..., led3: bool = ...) -> None: ...
