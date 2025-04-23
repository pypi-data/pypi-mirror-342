from make87_messages_ros2.rolling.autoware_map_msgs.msg import point_cloud_map_cell_meta_data_pb2 as _point_cloud_map_cell_meta_data_pb2
from make87_messages_ros2.rolling.sensor_msgs.msg import point_cloud2_pb2 as _point_cloud2_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PointCloudMapCellWithID(_message.Message):
    __slots__ = ("cell_id", "pointcloud", "metadata")
    CELL_ID_FIELD_NUMBER: _ClassVar[int]
    POINTCLOUD_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    cell_id: str
    pointcloud: _point_cloud2_pb2.PointCloud2
    metadata: _point_cloud_map_cell_meta_data_pb2.PointCloudMapCellMetaData
    def __init__(self, cell_id: _Optional[str] = ..., pointcloud: _Optional[_Union[_point_cloud2_pb2.PointCloud2, _Mapping]] = ..., metadata: _Optional[_Union[_point_cloud_map_cell_meta_data_pb2.PointCloudMapCellMetaData, _Mapping]] = ...) -> None: ...
