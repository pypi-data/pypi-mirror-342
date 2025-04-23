from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GimbalManagerConfigureRequest(_message.Message):
    __slots__ = ("sysid_primary", "compid_primary", "sysid_secondary", "compid_secondary", "gimbal_device_id")
    SYSID_PRIMARY_FIELD_NUMBER: _ClassVar[int]
    COMPID_PRIMARY_FIELD_NUMBER: _ClassVar[int]
    SYSID_SECONDARY_FIELD_NUMBER: _ClassVar[int]
    COMPID_SECONDARY_FIELD_NUMBER: _ClassVar[int]
    GIMBAL_DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    sysid_primary: int
    compid_primary: int
    sysid_secondary: int
    compid_secondary: int
    gimbal_device_id: int
    def __init__(self, sysid_primary: _Optional[int] = ..., compid_primary: _Optional[int] = ..., sysid_secondary: _Optional[int] = ..., compid_secondary: _Optional[int] = ..., gimbal_device_id: _Optional[int] = ...) -> None: ...

class GimbalManagerConfigureResponse(_message.Message):
    __slots__ = ("success", "result")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    success: bool
    result: int
    def __init__(self, success: bool = ..., result: _Optional[int] = ...) -> None: ...
