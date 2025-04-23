from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MrrStatusSwVersion(_message.Message):
    __slots__ = ("header", "can_pbl_field_revision", "can_pbl_promote_revision", "can_sw_field_revision", "can_sw_promote_revision", "can_sw_release_revision", "can_pbl_release_revision")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CAN_PBL_FIELD_REVISION_FIELD_NUMBER: _ClassVar[int]
    CAN_PBL_PROMOTE_REVISION_FIELD_NUMBER: _ClassVar[int]
    CAN_SW_FIELD_REVISION_FIELD_NUMBER: _ClassVar[int]
    CAN_SW_PROMOTE_REVISION_FIELD_NUMBER: _ClassVar[int]
    CAN_SW_RELEASE_REVISION_FIELD_NUMBER: _ClassVar[int]
    CAN_PBL_RELEASE_REVISION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    can_pbl_field_revision: int
    can_pbl_promote_revision: int
    can_sw_field_revision: int
    can_sw_promote_revision: int
    can_sw_release_revision: int
    can_pbl_release_revision: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., can_pbl_field_revision: _Optional[int] = ..., can_pbl_promote_revision: _Optional[int] = ..., can_sw_field_revision: _Optional[int] = ..., can_sw_promote_revision: _Optional[int] = ..., can_sw_release_revision: _Optional[int] = ..., can_pbl_release_revision: _Optional[int] = ...) -> None: ...
