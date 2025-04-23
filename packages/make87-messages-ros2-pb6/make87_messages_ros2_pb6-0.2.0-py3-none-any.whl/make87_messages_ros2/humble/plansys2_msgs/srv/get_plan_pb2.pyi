from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.plansys2_msgs.msg import plan_pb2 as _plan_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetPlanRequest(_message.Message):
    __slots__ = ("header", "domain", "problem")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    PROBLEM_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    domain: str
    problem: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., domain: _Optional[str] = ..., problem: _Optional[str] = ...) -> None: ...

class GetPlanResponse(_message.Message):
    __slots__ = ("header", "success", "plan", "error_info")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    PLAN_FIELD_NUMBER: _ClassVar[int]
    ERROR_INFO_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    plan: _plan_pb2.Plan
    error_info: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., plan: _Optional[_Union[_plan_pb2.Plan, _Mapping]] = ..., error_info: _Optional[str] = ...) -> None: ...
