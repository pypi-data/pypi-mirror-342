from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.plansys2_msgs.msg import durative_action_pb2 as _durative_action_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetDomainDurativeActionDetailsRequest(_message.Message):
    __slots__ = ("header", "durative_action", "parameters")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DURATIVE_ACTION_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    durative_action: str
    parameters: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., durative_action: _Optional[str] = ..., parameters: _Optional[_Iterable[str]] = ...) -> None: ...

class GetDomainDurativeActionDetailsResponse(_message.Message):
    __slots__ = ("header", "success", "durative_action", "error_info")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    DURATIVE_ACTION_FIELD_NUMBER: _ClassVar[int]
    ERROR_INFO_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    durative_action: _durative_action_pb2.DurativeAction
    error_info: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., durative_action: _Optional[_Union[_durative_action_pb2.DurativeAction, _Mapping]] = ..., error_info: _Optional[str] = ...) -> None: ...
