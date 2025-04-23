from make87_messages_ros2.jazzy.std_msgs.msg import color_rgba_pb2 as _color_rgba_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LeftEyeLeds(_message.Message):
    __slots__ = ("colors",)
    COLORS_FIELD_NUMBER: _ClassVar[int]
    colors: _containers.RepeatedCompositeFieldContainer[_color_rgba_pb2.ColorRGBA]
    def __init__(self, colors: _Optional[_Iterable[_Union[_color_rgba_pb2.ColorRGBA, _Mapping]]] = ...) -> None: ...
