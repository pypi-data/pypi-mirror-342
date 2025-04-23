from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.gazebo_msgs.msg import ode_joint_properties_pb2 as _ode_joint_properties_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetJointPropertiesRequest(_message.Message):
    __slots__ = ("header", "joint_name", "ode_joint_config")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    JOINT_NAME_FIELD_NUMBER: _ClassVar[int]
    ODE_JOINT_CONFIG_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    joint_name: str
    ode_joint_config: _ode_joint_properties_pb2.ODEJointProperties
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., joint_name: _Optional[str] = ..., ode_joint_config: _Optional[_Union[_ode_joint_properties_pb2.ODEJointProperties, _Mapping]] = ...) -> None: ...

class SetJointPropertiesResponse(_message.Message):
    __slots__ = ("header", "success", "status_message")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    status_message: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., status_message: _Optional[str] = ...) -> None: ...
