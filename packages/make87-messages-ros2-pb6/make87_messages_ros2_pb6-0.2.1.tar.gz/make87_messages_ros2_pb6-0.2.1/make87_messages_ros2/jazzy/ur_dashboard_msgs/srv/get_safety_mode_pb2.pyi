from make87_messages_ros2.jazzy.ur_dashboard_msgs.msg import safety_mode_pb2 as _safety_mode_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetSafetyModeRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetSafetyModeResponse(_message.Message):
    __slots__ = ("safety_mode", "answer", "success")
    SAFETY_MODE_FIELD_NUMBER: _ClassVar[int]
    ANSWER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    safety_mode: _safety_mode_pb2.SafetyMode
    answer: str
    success: bool
    def __init__(self, safety_mode: _Optional[_Union[_safety_mode_pb2.SafetyMode, _Mapping]] = ..., answer: _Optional[str] = ..., success: bool = ...) -> None: ...
