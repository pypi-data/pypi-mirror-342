from make87_messages_ros2.jazzy.rcl_interfaces.msg import parameter_value_pb2 as _parameter_value_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ParamSetV2Request(_message.Message):
    __slots__ = ("force_set", "param_id", "value")
    FORCE_SET_FIELD_NUMBER: _ClassVar[int]
    PARAM_ID_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    force_set: bool
    param_id: str
    value: _parameter_value_pb2.ParameterValue
    def __init__(self, force_set: bool = ..., param_id: _Optional[str] = ..., value: _Optional[_Union[_parameter_value_pb2.ParameterValue, _Mapping]] = ...) -> None: ...

class ParamSetV2Response(_message.Message):
    __slots__ = ("success", "value")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    value: _parameter_value_pb2.ParameterValue
    def __init__(self, success: bool = ..., value: _Optional[_Union[_parameter_value_pb2.ParameterValue, _Mapping]] = ...) -> None: ...
