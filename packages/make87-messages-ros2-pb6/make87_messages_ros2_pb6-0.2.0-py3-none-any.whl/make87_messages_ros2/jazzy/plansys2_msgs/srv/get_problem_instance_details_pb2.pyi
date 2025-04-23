from make87_messages_ros2.jazzy.plansys2_msgs.msg import param_pb2 as _param_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetProblemInstanceDetailsRequest(_message.Message):
    __slots__ = ("instance",)
    INSTANCE_FIELD_NUMBER: _ClassVar[int]
    instance: str
    def __init__(self, instance: _Optional[str] = ...) -> None: ...

class GetProblemInstanceDetailsResponse(_message.Message):
    __slots__ = ("success", "instance", "error_info")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_FIELD_NUMBER: _ClassVar[int]
    ERROR_INFO_FIELD_NUMBER: _ClassVar[int]
    success: bool
    instance: _param_pb2.Param
    error_info: str
    def __init__(self, success: bool = ..., instance: _Optional[_Union[_param_pb2.Param, _Mapping]] = ..., error_info: _Optional[str] = ...) -> None: ...
