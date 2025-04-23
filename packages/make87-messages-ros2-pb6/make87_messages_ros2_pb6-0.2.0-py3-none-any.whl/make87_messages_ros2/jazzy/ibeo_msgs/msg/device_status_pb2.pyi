from make87_messages_ros2.jazzy.ibeo_msgs.msg import ibeo_data_header_pb2 as _ibeo_data_header_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DeviceStatus(_message.Message):
    __slots__ = ("header", "ibeo_header", "scanner_type", "sensor_temperature", "frequency")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    IBEO_HEADER_FIELD_NUMBER: _ClassVar[int]
    SCANNER_TYPE_FIELD_NUMBER: _ClassVar[int]
    SENSOR_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ibeo_header: _ibeo_data_header_pb2.IbeoDataHeader
    scanner_type: int
    sensor_temperature: float
    frequency: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ibeo_header: _Optional[_Union[_ibeo_data_header_pb2.IbeoDataHeader, _Mapping]] = ..., scanner_type: _Optional[int] = ..., sensor_temperature: _Optional[float] = ..., frequency: _Optional[float] = ...) -> None: ...
