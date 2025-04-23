from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.humble.rmf_workcell_msgs.msg import asset_pb2 as _asset_pb2
from make87_messages_ros2.humble.rmf_workcell_msgs.msg import trait_pb2 as _trait_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class WorkcellConfiguration(_message.Message):
    __slots__ = ("header", "time", "guid", "type", "assets", "traits")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    GUID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ASSETS_FIELD_NUMBER: _ClassVar[int]
    TRAITS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    time: _time_pb2.Time
    guid: str
    type: str
    assets: _containers.RepeatedCompositeFieldContainer[_asset_pb2.Asset]
    traits: _containers.RepeatedCompositeFieldContainer[_trait_pb2.Trait]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., guid: _Optional[str] = ..., type: _Optional[str] = ..., assets: _Optional[_Iterable[_Union[_asset_pb2.Asset, _Mapping]]] = ..., traits: _Optional[_Iterable[_Union[_trait_pb2.Trait, _Mapping]]] = ...) -> None: ...
