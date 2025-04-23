from make87_messages_ros2.jazzy.rtabmap_msgs.msg import link_pb2 as _link_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AddLinkRequest(_message.Message):
    __slots__ = ("link",)
    LINK_FIELD_NUMBER: _ClassVar[int]
    link: _link_pb2.Link
    def __init__(self, link: _Optional[_Union[_link_pb2.Link, _Mapping]] = ...) -> None: ...

class AddLinkResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
