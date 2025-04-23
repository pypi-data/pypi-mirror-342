from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from make87_messages_ros2.rolling.tuw_multi_robot_msgs.msg import station_pb2 as _station_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StationArray(_message.Message):
    __slots__ = ("header", "stations")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STATIONS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    stations: _containers.RepeatedCompositeFieldContainer[_station_pb2.Station]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., stations: _Optional[_Iterable[_Union[_station_pb2.Station, _Mapping]]] = ...) -> None: ...
