from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.autoware_map_msgs.msg import point_cloud_map_cell_meta_data_with_id_pb2 as _point_cloud_map_cell_meta_data_with_id_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PointCloudMapMetaData(_message.Message):
    __slots__ = ("header", "ros2_header", "metadata_list")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    METADATA_LIST_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    metadata_list: _containers.RepeatedCompositeFieldContainer[_point_cloud_map_cell_meta_data_with_id_pb2.PointCloudMapCellMetaDataWithID]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., metadata_list: _Optional[_Iterable[_Union[_point_cloud_map_cell_meta_data_with_id_pb2.PointCloudMapCellMetaDataWithID, _Mapping]]] = ...) -> None: ...
