from make87_messages_ros2.rolling.autoware_map_msgs.msg import lanelet_map_bin_pb2 as _lanelet_map_bin_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetSelectedLanelet2MapRequest(_message.Message):
    __slots__ = ("cell_ids",)
    CELL_IDS_FIELD_NUMBER: _ClassVar[int]
    cell_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, cell_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class GetSelectedLanelet2MapResponse(_message.Message):
    __slots__ = ("header", "lanelet2_cells")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LANELET2_CELLS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    lanelet2_cells: _lanelet_map_bin_pb2.LaneletMapBin
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., lanelet2_cells: _Optional[_Union[_lanelet_map_bin_pb2.LaneletMapBin, _Mapping]] = ...) -> None: ...
