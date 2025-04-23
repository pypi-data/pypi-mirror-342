from make87_messages_ros2.jazzy.rc_reason_msgs.msg import range_box_pb2 as _range_box_pb2
from make87_messages_ros2.jazzy.rc_reason_msgs.msg import range_rectangle_pb2 as _range_rectangle_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ItemModel(_message.Message):
    __slots__ = ("type", "unknown", "rectangle")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN_FIELD_NUMBER: _ClassVar[int]
    RECTANGLE_FIELD_NUMBER: _ClassVar[int]
    type: str
    unknown: _range_box_pb2.RangeBox
    rectangle: _range_rectangle_pb2.RangeRectangle
    def __init__(self, type: _Optional[str] = ..., unknown: _Optional[_Union[_range_box_pb2.RangeBox, _Mapping]] = ..., rectangle: _Optional[_Union[_range_rectangle_pb2.RangeRectangle, _Mapping]] = ...) -> None: ...
