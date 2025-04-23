from make87_messages_ros2.rolling.rcl_interfaces.msg import parameter_pb2 as _parameter_pb2
from make87_messages_ros2.rolling.rcl_interfaces.msg import set_parameters_result_pb2 as _set_parameters_result_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetParametersAtomicallyRequest(_message.Message):
    __slots__ = ("parameters",)
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    parameters: _containers.RepeatedCompositeFieldContainer[_parameter_pb2.Parameter]
    def __init__(self, parameters: _Optional[_Iterable[_Union[_parameter_pb2.Parameter, _Mapping]]] = ...) -> None: ...

class SetParametersAtomicallyResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: _set_parameters_result_pb2.SetParametersResult
    def __init__(self, result: _Optional[_Union[_set_parameters_result_pb2.SetParametersResult, _Mapping]] = ...) -> None: ...
