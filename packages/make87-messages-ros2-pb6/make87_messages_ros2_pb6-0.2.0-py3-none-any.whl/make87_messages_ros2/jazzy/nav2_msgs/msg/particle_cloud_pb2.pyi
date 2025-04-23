from make87_messages_ros2.jazzy.nav2_msgs.msg import particle_pb2 as _particle_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ParticleCloud(_message.Message):
    __slots__ = ("header", "particles")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PARTICLES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    particles: _containers.RepeatedCompositeFieldContainer[_particle_pb2.Particle]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., particles: _Optional[_Iterable[_Union[_particle_pb2.Particle, _Mapping]]] = ...) -> None: ...
