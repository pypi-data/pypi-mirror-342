from make87_messages_ros2.rolling.mavros_msgs.msg import esc_telemetry_item_pb2 as _esc_telemetry_item_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ESCTelemetry(_message.Message):
    __slots__ = ("header", "esc_telemetry")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ESC_TELEMETRY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    esc_telemetry: _containers.RepeatedCompositeFieldContainer[_esc_telemetry_item_pb2.ESCTelemetryItem]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., esc_telemetry: _Optional[_Iterable[_Union[_esc_telemetry_item_pb2.ESCTelemetryItem, _Mapping]]] = ...) -> None: ...
