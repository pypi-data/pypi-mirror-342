from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AccessPoint(_message.Message):
    __slots__ = ("header", "ros2_header", "essid", "macaddr", "signal", "noise", "snr", "channel", "rate", "tx_power", "quality")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    ESSID_FIELD_NUMBER: _ClassVar[int]
    MACADDR_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_FIELD_NUMBER: _ClassVar[int]
    NOISE_FIELD_NUMBER: _ClassVar[int]
    SNR_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    RATE_FIELD_NUMBER: _ClassVar[int]
    TX_POWER_FIELD_NUMBER: _ClassVar[int]
    QUALITY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    essid: str
    macaddr: str
    signal: int
    noise: int
    snr: int
    channel: int
    rate: str
    tx_power: str
    quality: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., essid: _Optional[str] = ..., macaddr: _Optional[str] = ..., signal: _Optional[int] = ..., noise: _Optional[int] = ..., snr: _Optional[int] = ..., channel: _Optional[int] = ..., rate: _Optional[str] = ..., tx_power: _Optional[str] = ..., quality: _Optional[int] = ...) -> None: ...
