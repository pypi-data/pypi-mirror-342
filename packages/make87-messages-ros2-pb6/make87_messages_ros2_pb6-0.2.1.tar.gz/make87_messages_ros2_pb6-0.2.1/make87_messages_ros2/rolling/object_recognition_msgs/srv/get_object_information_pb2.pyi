from make87_messages_ros2.rolling.object_recognition_msgs.msg import object_information_pb2 as _object_information_pb2
from make87_messages_ros2.rolling.object_recognition_msgs.msg import object_type_pb2 as _object_type_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetObjectInformationRequest(_message.Message):
    __slots__ = ("type",)
    TYPE_FIELD_NUMBER: _ClassVar[int]
    type: _object_type_pb2.ObjectType
    def __init__(self, type: _Optional[_Union[_object_type_pb2.ObjectType, _Mapping]] = ...) -> None: ...

class GetObjectInformationResponse(_message.Message):
    __slots__ = ("information",)
    INFORMATION_FIELD_NUMBER: _ClassVar[int]
    information: _object_information_pb2.ObjectInformation
    def __init__(self, information: _Optional[_Union[_object_information_pb2.ObjectInformation, _Mapping]] = ...) -> None: ...
