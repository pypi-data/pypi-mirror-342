from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.map_msgs.msg import projected_map_info_pb2 as _projected_map_info_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetMapProjectionsRequest(_message.Message):
    __slots__ = ("header",)
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...

class SetMapProjectionsResponse(_message.Message):
    __slots__ = ("header", "projected_maps_info")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PROJECTED_MAPS_INFO_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    projected_maps_info: _containers.RepeatedCompositeFieldContainer[_projected_map_info_pb2.ProjectedMapInfo]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., projected_maps_info: _Optional[_Iterable[_Union[_projected_map_info_pb2.ProjectedMapInfo, _Mapping]]] = ...) -> None: ...
