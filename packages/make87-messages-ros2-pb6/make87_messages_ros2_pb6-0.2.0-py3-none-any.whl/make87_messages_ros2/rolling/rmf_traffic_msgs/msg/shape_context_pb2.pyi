from make87_messages_ros2.rolling.rmf_traffic_msgs.msg import convex_shape_context_pb2 as _convex_shape_context_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ShapeContext(_message.Message):
    __slots__ = ("convex_shapes",)
    CONVEX_SHAPES_FIELD_NUMBER: _ClassVar[int]
    convex_shapes: _convex_shape_context_pb2.ConvexShapeContext
    def __init__(self, convex_shapes: _Optional[_Union[_convex_shape_context_pb2.ConvexShapeContext, _Mapping]] = ...) -> None: ...
