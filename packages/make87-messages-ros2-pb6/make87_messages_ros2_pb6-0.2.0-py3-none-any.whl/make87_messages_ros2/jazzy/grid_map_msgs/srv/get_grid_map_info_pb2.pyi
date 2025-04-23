from make87_messages_ros2.jazzy.grid_map_msgs.msg import grid_map_info_pb2 as _grid_map_info_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetGridMapInfoRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetGridMapInfoResponse(_message.Message):
    __slots__ = ("info",)
    INFO_FIELD_NUMBER: _ClassVar[int]
    info: _grid_map_info_pb2.GridMapInfo
    def __init__(self, info: _Optional[_Union[_grid_map_info_pb2.GridMapInfo, _Mapping]] = ...) -> None: ...
