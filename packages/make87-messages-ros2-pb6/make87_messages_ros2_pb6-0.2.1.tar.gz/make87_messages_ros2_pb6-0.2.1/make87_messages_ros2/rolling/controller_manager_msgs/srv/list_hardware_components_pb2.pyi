from make87_messages_ros2.rolling.controller_manager_msgs.msg import hardware_component_state_pb2 as _hardware_component_state_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ListHardwareComponentsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListHardwareComponentsResponse(_message.Message):
    __slots__ = ("component",)
    COMPONENT_FIELD_NUMBER: _ClassVar[int]
    component: _containers.RepeatedCompositeFieldContainer[_hardware_component_state_pb2.HardwareComponentState]
    def __init__(self, component: _Optional[_Iterable[_Union[_hardware_component_state_pb2.HardwareComponentState, _Mapping]]] = ...) -> None: ...
