from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.moveit_msgs.msg import motion_sequence_item_pb2 as _motion_sequence_item_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MotionSequenceRequest(_message.Message):
    __slots__ = ("header", "items")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    items: _containers.RepeatedCompositeFieldContainer[_motion_sequence_item_pb2.MotionSequenceItem]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., items: _Optional[_Iterable[_Union[_motion_sequence_item_pb2.MotionSequenceItem, _Mapping]]] = ...) -> None: ...
