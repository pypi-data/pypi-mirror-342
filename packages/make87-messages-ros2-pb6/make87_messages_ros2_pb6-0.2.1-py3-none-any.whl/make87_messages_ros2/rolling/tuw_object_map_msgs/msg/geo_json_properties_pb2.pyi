from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GeoJSONProperties(_message.Message):
    __slots__ = ("id", "type", "enflation_radius", "bondary_radius")
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ENFLATION_RADIUS_FIELD_NUMBER: _ClassVar[int]
    BONDARY_RADIUS_FIELD_NUMBER: _ClassVar[int]
    id: int
    type: int
    enflation_radius: _containers.RepeatedScalarFieldContainer[float]
    bondary_radius: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, id: _Optional[int] = ..., type: _Optional[int] = ..., enflation_radius: _Optional[_Iterable[float]] = ..., bondary_radius: _Optional[_Iterable[float]] = ...) -> None: ...
