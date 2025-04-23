from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.grid_map_msgs.msg import grid_map_info_pb2 as _grid_map_info_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetGridMapInfoRequest(_message.Message):
    __slots__ = ("header",)
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...

class GetGridMapInfoResponse(_message.Message):
    __slots__ = ("header", "info")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    info: _grid_map_info_pb2.GridMapInfo
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., info: _Optional[_Union[_grid_map_info_pb2.GridMapInfo, _Mapping]] = ...) -> None: ...
