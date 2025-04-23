from make87_messages_ros2.rolling.visualization_msgs.msg import interactive_marker_pb2 as _interactive_marker_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetInteractiveMarkersRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetInteractiveMarkersResponse(_message.Message):
    __slots__ = ("sequence_number", "markers")
    SEQUENCE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    MARKERS_FIELD_NUMBER: _ClassVar[int]
    sequence_number: int
    markers: _containers.RepeatedCompositeFieldContainer[_interactive_marker_pb2.InteractiveMarker]
    def __init__(self, sequence_number: _Optional[int] = ..., markers: _Optional[_Iterable[_Union[_interactive_marker_pb2.InteractiveMarker, _Mapping]]] = ...) -> None: ...
