from make87_messages_ros2.rolling.moveit_msgs.msg import move_it_error_codes_pb2 as _move_it_error_codes_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetGroupUrdfRequest(_message.Message):
    __slots__ = ("group_name",)
    GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    group_name: str
    def __init__(self, group_name: _Optional[str] = ...) -> None: ...

class GetGroupUrdfResponse(_message.Message):
    __slots__ = ("error_code", "urdf_string")
    ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    URDF_STRING_FIELD_NUMBER: _ClassVar[int]
    error_code: _move_it_error_codes_pb2.MoveItErrorCodes
    urdf_string: str
    def __init__(self, error_code: _Optional[_Union[_move_it_error_codes_pb2.MoveItErrorCodes, _Mapping]] = ..., urdf_string: _Optional[str] = ...) -> None: ...
