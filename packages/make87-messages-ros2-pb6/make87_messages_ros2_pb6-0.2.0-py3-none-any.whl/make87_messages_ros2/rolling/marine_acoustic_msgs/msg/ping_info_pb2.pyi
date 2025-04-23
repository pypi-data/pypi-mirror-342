from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PingInfo(_message.Message):
    __slots__ = ("frequency", "sound_speed", "tx_beamwidths", "rx_beamwidths")
    FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    SOUND_SPEED_FIELD_NUMBER: _ClassVar[int]
    TX_BEAMWIDTHS_FIELD_NUMBER: _ClassVar[int]
    RX_BEAMWIDTHS_FIELD_NUMBER: _ClassVar[int]
    frequency: float
    sound_speed: float
    tx_beamwidths: _containers.RepeatedScalarFieldContainer[float]
    rx_beamwidths: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, frequency: _Optional[float] = ..., sound_speed: _Optional[float] = ..., tx_beamwidths: _Optional[_Iterable[float]] = ..., rx_beamwidths: _Optional[_Iterable[float]] = ...) -> None: ...
