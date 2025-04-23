from make87_messages_ros2.rolling.rmf_traffic_msgs.msg import circle_pb2 as _circle_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ConvexShapeContext(_message.Message):
    __slots__ = ("circles",)
    CIRCLES_FIELD_NUMBER: _ClassVar[int]
    circles: _containers.RepeatedCompositeFieldContainer[_circle_pb2.Circle]
    def __init__(self, circles: _Optional[_Iterable[_Union[_circle_pb2.Circle, _Mapping]]] = ...) -> None: ...
