from make87_messages_ros2.rolling.irobot_create_msgs.msg import button_pb2 as _button_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class InterfaceButtons(_message.Message):
    __slots__ = ("header", "button_1", "button_power", "button_2")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BUTTON_1_FIELD_NUMBER: _ClassVar[int]
    BUTTON_POWER_FIELD_NUMBER: _ClassVar[int]
    BUTTON_2_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    button_1: _button_pb2.Button
    button_power: _button_pb2.Button
    button_2: _button_pb2.Button
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., button_1: _Optional[_Union[_button_pb2.Button, _Mapping]] = ..., button_power: _Optional[_Union[_button_pb2.Button, _Mapping]] = ..., button_2: _Optional[_Union[_button_pb2.Button, _Mapping]] = ...) -> None: ...
