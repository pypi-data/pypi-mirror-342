from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.autoware_map_msgs.msg import lanelet_map_bin_pb2 as _lanelet_map_bin_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetSelectedLanelet2MapRequest(_message.Message):
    __slots__ = ("header", "cell_ids")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CELL_IDS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    cell_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., cell_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class GetSelectedLanelet2MapResponse(_message.Message):
    __slots__ = ("header", "ros2_header", "lanelet2_cells")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    LANELET2_CELLS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    lanelet2_cells: _lanelet_map_bin_pb2.LaneletMapBin
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., lanelet2_cells: _Optional[_Union[_lanelet_map_bin_pb2.LaneletMapBin, _Mapping]] = ...) -> None: ...
