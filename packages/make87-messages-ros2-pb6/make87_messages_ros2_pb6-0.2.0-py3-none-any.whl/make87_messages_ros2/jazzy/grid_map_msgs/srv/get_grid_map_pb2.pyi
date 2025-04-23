from make87_messages_ros2.jazzy.grid_map_msgs.msg import grid_map_pb2 as _grid_map_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetGridMapRequest(_message.Message):
    __slots__ = ("frame_id", "position_x", "position_y", "length_x", "length_y", "layers")
    FRAME_ID_FIELD_NUMBER: _ClassVar[int]
    POSITION_X_FIELD_NUMBER: _ClassVar[int]
    POSITION_Y_FIELD_NUMBER: _ClassVar[int]
    LENGTH_X_FIELD_NUMBER: _ClassVar[int]
    LENGTH_Y_FIELD_NUMBER: _ClassVar[int]
    LAYERS_FIELD_NUMBER: _ClassVar[int]
    frame_id: str
    position_x: float
    position_y: float
    length_x: float
    length_y: float
    layers: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, frame_id: _Optional[str] = ..., position_x: _Optional[float] = ..., position_y: _Optional[float] = ..., length_x: _Optional[float] = ..., length_y: _Optional[float] = ..., layers: _Optional[_Iterable[str]] = ...) -> None: ...

class GetGridMapResponse(_message.Message):
    __slots__ = ("map",)
    MAP_FIELD_NUMBER: _ClassVar[int]
    map: _grid_map_pb2.GridMap
    def __init__(self, map: _Optional[_Union[_grid_map_pb2.GridMap, _Mapping]] = ...) -> None: ...
