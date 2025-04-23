from make87_messages_ros2.jazzy.geometry_msgs.msg import pose_stamped_pb2 as _pose_stamped_pb2
from make87_messages_ros2.jazzy.rc_reason_msgs.msg import box_pb2 as _box_pb2
from make87_messages_ros2.jazzy.rc_reason_msgs.msg import cell_filling_level_pb2 as _cell_filling_level_pb2
from make87_messages_ros2.jazzy.rc_reason_msgs.msg import grid_size_pb2 as _grid_size_pb2
from make87_messages_ros2.jazzy.rc_reason_msgs.msg import rectangle_pb2 as _rectangle_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LoadCarrierWithFillingLevel(_message.Message):
    __slots__ = ("id", "type", "outer_dimensions", "inner_dimensions", "rim_thickness", "rim_step_height", "rim_ledge", "height_open_side", "pose", "overfilled", "overall_filling_level", "cells_filling_levels", "filling_level_cell_count")
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    OUTER_DIMENSIONS_FIELD_NUMBER: _ClassVar[int]
    INNER_DIMENSIONS_FIELD_NUMBER: _ClassVar[int]
    RIM_THICKNESS_FIELD_NUMBER: _ClassVar[int]
    RIM_STEP_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    RIM_LEDGE_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_OPEN_SIDE_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    OVERFILLED_FIELD_NUMBER: _ClassVar[int]
    OVERALL_FILLING_LEVEL_FIELD_NUMBER: _ClassVar[int]
    CELLS_FILLING_LEVELS_FIELD_NUMBER: _ClassVar[int]
    FILLING_LEVEL_CELL_COUNT_FIELD_NUMBER: _ClassVar[int]
    id: str
    type: str
    outer_dimensions: _box_pb2.Box
    inner_dimensions: _box_pb2.Box
    rim_thickness: _rectangle_pb2.Rectangle
    rim_step_height: float
    rim_ledge: _rectangle_pb2.Rectangle
    height_open_side: float
    pose: _pose_stamped_pb2.PoseStamped
    overfilled: bool
    overall_filling_level: _cell_filling_level_pb2.CellFillingLevel
    cells_filling_levels: _containers.RepeatedCompositeFieldContainer[_cell_filling_level_pb2.CellFillingLevel]
    filling_level_cell_count: _grid_size_pb2.GridSize
    def __init__(self, id: _Optional[str] = ..., type: _Optional[str] = ..., outer_dimensions: _Optional[_Union[_box_pb2.Box, _Mapping]] = ..., inner_dimensions: _Optional[_Union[_box_pb2.Box, _Mapping]] = ..., rim_thickness: _Optional[_Union[_rectangle_pb2.Rectangle, _Mapping]] = ..., rim_step_height: _Optional[float] = ..., rim_ledge: _Optional[_Union[_rectangle_pb2.Rectangle, _Mapping]] = ..., height_open_side: _Optional[float] = ..., pose: _Optional[_Union[_pose_stamped_pb2.PoseStamped, _Mapping]] = ..., overfilled: bool = ..., overall_filling_level: _Optional[_Union[_cell_filling_level_pb2.CellFillingLevel, _Mapping]] = ..., cells_filling_levels: _Optional[_Iterable[_Union[_cell_filling_level_pb2.CellFillingLevel, _Mapping]]] = ..., filling_level_cell_count: _Optional[_Union[_grid_size_pb2.GridSize, _Mapping]] = ...) -> None: ...
