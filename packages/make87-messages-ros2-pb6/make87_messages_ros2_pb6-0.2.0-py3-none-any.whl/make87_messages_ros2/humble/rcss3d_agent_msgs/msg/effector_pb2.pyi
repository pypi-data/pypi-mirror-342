from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rcss3d_agent_msgs.msg import beam_pb2 as _beam_pb2
from make87_messages_ros2.humble.rcss3d_agent_msgs.msg import hinge_joint_vel_pb2 as _hinge_joint_vel_pb2
from make87_messages_ros2.humble.rcss3d_agent_msgs.msg import say_pb2 as _say_pb2
from make87_messages_ros2.humble.rcss3d_agent_msgs.msg import universal_joint_vel_pb2 as _universal_joint_vel_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Effector(_message.Message):
    __slots__ = ("header", "hinge_joint_vels", "universal_joint_vels", "beams", "says")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    HINGE_JOINT_VELS_FIELD_NUMBER: _ClassVar[int]
    UNIVERSAL_JOINT_VELS_FIELD_NUMBER: _ClassVar[int]
    BEAMS_FIELD_NUMBER: _ClassVar[int]
    SAYS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    hinge_joint_vels: _containers.RepeatedCompositeFieldContainer[_hinge_joint_vel_pb2.HingeJointVel]
    universal_joint_vels: _containers.RepeatedCompositeFieldContainer[_universal_joint_vel_pb2.UniversalJointVel]
    beams: _containers.RepeatedCompositeFieldContainer[_beam_pb2.Beam]
    says: _containers.RepeatedCompositeFieldContainer[_say_pb2.Say]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., hinge_joint_vels: _Optional[_Iterable[_Union[_hinge_joint_vel_pb2.HingeJointVel, _Mapping]]] = ..., universal_joint_vels: _Optional[_Iterable[_Union[_universal_joint_vel_pb2.UniversalJointVel, _Mapping]]] = ..., beams: _Optional[_Iterable[_Union[_beam_pb2.Beam, _Mapping]]] = ..., says: _Optional[_Iterable[_Union[_say_pb2.Say, _Mapping]]] = ...) -> None: ...
