from make87_messages_ros2.rolling.std_msgs.msg import color_rgba_pb2 as _color_rgba_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ObjectColor(_message.Message):
    __slots__ = ("id", "color")
    ID_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    id: str
    color: _color_rgba_pb2.ColorRGBA
    def __init__(self, id: _Optional[str] = ..., color: _Optional[_Union[_color_rgba_pb2.ColorRGBA, _Mapping]] = ...) -> None: ...
