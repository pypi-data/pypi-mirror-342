from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SensorEthernetConfigurationInformation(_message.Message):
    __slots__ = ("header", "sensor_ip_address", "destination_ip_address", "netmask", "vlan", "source_port", "destination_port")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SENSOR_IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    NETMASK_FIELD_NUMBER: _ClassVar[int]
    VLAN_FIELD_NUMBER: _ClassVar[int]
    SOURCE_PORT_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_PORT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    sensor_ip_address: str
    destination_ip_address: str
    netmask: str
    vlan: int
    source_port: int
    destination_port: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., sensor_ip_address: _Optional[str] = ..., destination_ip_address: _Optional[str] = ..., netmask: _Optional[str] = ..., vlan: _Optional[int] = ..., source_port: _Optional[int] = ..., destination_port: _Optional[int] = ...) -> None: ...
