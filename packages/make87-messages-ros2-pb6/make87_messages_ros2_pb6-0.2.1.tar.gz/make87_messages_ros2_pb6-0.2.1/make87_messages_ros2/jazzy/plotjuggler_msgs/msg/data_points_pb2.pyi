from make87_messages_ros2.jazzy.plotjuggler_msgs.msg import data_point_pb2 as _data_point_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DataPoints(_message.Message):
    __slots__ = ("dictionary_uuid", "samples")
    DICTIONARY_UUID_FIELD_NUMBER: _ClassVar[int]
    SAMPLES_FIELD_NUMBER: _ClassVar[int]
    dictionary_uuid: int
    samples: _containers.RepeatedCompositeFieldContainer[_data_point_pb2.DataPoint]
    def __init__(self, dictionary_uuid: _Optional[int] = ..., samples: _Optional[_Iterable[_Union[_data_point_pb2.DataPoint, _Mapping]]] = ...) -> None: ...
