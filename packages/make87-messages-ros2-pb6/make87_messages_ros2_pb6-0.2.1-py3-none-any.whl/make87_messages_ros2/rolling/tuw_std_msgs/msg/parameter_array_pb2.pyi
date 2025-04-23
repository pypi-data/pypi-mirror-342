from make87_messages_ros2.rolling.tuw_std_msgs.msg import parameter_pb2 as _parameter_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ParameterArray(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[_parameter_pb2.Parameter]
    def __init__(self, data: _Optional[_Iterable[_Union[_parameter_pb2.Parameter, _Mapping]]] = ...) -> None: ...
