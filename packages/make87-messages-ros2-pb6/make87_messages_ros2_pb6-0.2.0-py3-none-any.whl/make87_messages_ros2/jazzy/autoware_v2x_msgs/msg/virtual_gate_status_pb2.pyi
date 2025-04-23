from make87_messages_ros2.jazzy.autoware_v2x_msgs.msg import virtual_gate_area_status_pb2 as _virtual_gate_area_status_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VirtualGateStatus(_message.Message):
    __slots__ = ("areas",)
    AREAS_FIELD_NUMBER: _ClassVar[int]
    areas: _containers.RepeatedCompositeFieldContainer[_virtual_gate_area_status_pb2.VirtualGateAreaStatus]
    def __init__(self, areas: _Optional[_Iterable[_Union[_virtual_gate_area_status_pb2.VirtualGateAreaStatus, _Mapping]]] = ...) -> None: ...
