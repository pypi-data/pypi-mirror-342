from make87_messages_ros2.jazzy.rmf_traffic_msgs.msg import profile_pb2 as _profile_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ParticipantDescription(_message.Message):
    __slots__ = ("name", "owner", "responsiveness", "profile")
    NAME_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    RESPONSIVENESS_FIELD_NUMBER: _ClassVar[int]
    PROFILE_FIELD_NUMBER: _ClassVar[int]
    name: str
    owner: str
    responsiveness: int
    profile: _profile_pb2.Profile
    def __init__(self, name: _Optional[str] = ..., owner: _Optional[str] = ..., responsiveness: _Optional[int] = ..., profile: _Optional[_Union[_profile_pb2.Profile, _Mapping]] = ...) -> None: ...
