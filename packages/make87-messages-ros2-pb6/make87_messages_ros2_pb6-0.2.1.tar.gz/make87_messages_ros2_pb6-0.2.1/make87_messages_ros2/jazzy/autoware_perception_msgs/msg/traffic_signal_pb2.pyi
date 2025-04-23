from make87_messages_ros2.jazzy.autoware_perception_msgs.msg import traffic_signal_element_pb2 as _traffic_signal_element_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TrafficSignal(_message.Message):
    __slots__ = ("traffic_signal_id", "elements")
    TRAFFIC_SIGNAL_ID_FIELD_NUMBER: _ClassVar[int]
    ELEMENTS_FIELD_NUMBER: _ClassVar[int]
    traffic_signal_id: int
    elements: _containers.RepeatedCompositeFieldContainer[_traffic_signal_element_pb2.TrafficSignalElement]
    def __init__(self, traffic_signal_id: _Optional[int] = ..., elements: _Optional[_Iterable[_Union[_traffic_signal_element_pb2.TrafficSignalElement, _Mapping]]] = ...) -> None: ...
