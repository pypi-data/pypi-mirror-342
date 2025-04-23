from make87_messages_ros2.rolling.tuw_object_msgs.msg import shape_array_pb2 as _shape_array_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetShapeArrayRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetShapeArrayResponse(_message.Message):
    __slots__ = ("shapes",)
    SHAPES_FIELD_NUMBER: _ClassVar[int]
    shapes: _shape_array_pb2.ShapeArray
    def __init__(self, shapes: _Optional[_Union[_shape_array_pb2.ShapeArray, _Mapping]] = ...) -> None: ...
