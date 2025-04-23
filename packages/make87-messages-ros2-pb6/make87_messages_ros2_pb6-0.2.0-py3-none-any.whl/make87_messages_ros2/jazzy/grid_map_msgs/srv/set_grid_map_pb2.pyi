from make87_messages_ros2.jazzy.grid_map_msgs.msg import grid_map_pb2 as _grid_map_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetGridMapRequest(_message.Message):
    __slots__ = ("map",)
    MAP_FIELD_NUMBER: _ClassVar[int]
    map: _grid_map_pb2.GridMap
    def __init__(self, map: _Optional[_Union[_grid_map_pb2.GridMap, _Mapping]] = ...) -> None: ...

class SetGridMapResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
