from make87_messages_ros2.jazzy.plansys2_msgs.msg import durative_action_pb2 as _durative_action_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetDomainDurativeActionDetailsRequest(_message.Message):
    __slots__ = ("durative_action", "parameters")
    DURATIVE_ACTION_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    durative_action: str
    parameters: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, durative_action: _Optional[str] = ..., parameters: _Optional[_Iterable[str]] = ...) -> None: ...

class GetDomainDurativeActionDetailsResponse(_message.Message):
    __slots__ = ("success", "durative_action", "error_info")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    DURATIVE_ACTION_FIELD_NUMBER: _ClassVar[int]
    ERROR_INFO_FIELD_NUMBER: _ClassVar[int]
    success: bool
    durative_action: _durative_action_pb2.DurativeAction
    error_info: str
    def __init__(self, success: bool = ..., durative_action: _Optional[_Union[_durative_action_pb2.DurativeAction, _Mapping]] = ..., error_info: _Optional[str] = ...) -> None: ...
