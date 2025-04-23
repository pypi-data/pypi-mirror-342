from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SetModelConfigurationRequest(_message.Message):
    __slots__ = ("model_name", "urdf_param_name", "joint_names", "joint_positions")
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    URDF_PARAM_NAME_FIELD_NUMBER: _ClassVar[int]
    JOINT_NAMES_FIELD_NUMBER: _ClassVar[int]
    JOINT_POSITIONS_FIELD_NUMBER: _ClassVar[int]
    model_name: str
    urdf_param_name: str
    joint_names: _containers.RepeatedScalarFieldContainer[str]
    joint_positions: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, model_name: _Optional[str] = ..., urdf_param_name: _Optional[str] = ..., joint_names: _Optional[_Iterable[str]] = ..., joint_positions: _Optional[_Iterable[float]] = ...) -> None: ...

class SetModelConfigurationResponse(_message.Message):
    __slots__ = ("success", "status_message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    status_message: str
    def __init__(self, success: bool = ..., status_message: _Optional[str] = ...) -> None: ...
