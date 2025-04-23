from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.off_highway_premium_radar_sample_msgs.msg import diagnostics_ethernet_configuration_information_pb2 as _diagnostics_ethernet_configuration_information_pb2
from make87_messages_ros2.humble.off_highway_premium_radar_sample_msgs.msg import do_ip_information_pb2 as _do_ip_information_pb2
from make87_messages_ros2.humble.off_highway_premium_radar_sample_msgs.msg import sensor_ethernet_configuration_information_pb2 as _sensor_ethernet_configuration_information_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SensorBroadcastData(_message.Message):
    __slots__ = ("header", "customer_version", "sensor_ethernet_configuration_information", "diagnostics_ethernet_configuration_information", "sensor_mac_address", "doip_information")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_VERSION_FIELD_NUMBER: _ClassVar[int]
    SENSOR_ETHERNET_CONFIGURATION_INFORMATION_FIELD_NUMBER: _ClassVar[int]
    DIAGNOSTICS_ETHERNET_CONFIGURATION_INFORMATION_FIELD_NUMBER: _ClassVar[int]
    SENSOR_MAC_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    DOIP_INFORMATION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    customer_version: int
    sensor_ethernet_configuration_information: _sensor_ethernet_configuration_information_pb2.SensorEthernetConfigurationInformation
    diagnostics_ethernet_configuration_information: _diagnostics_ethernet_configuration_information_pb2.DiagnosticsEthernetConfigurationInformation
    sensor_mac_address: int
    doip_information: _do_ip_information_pb2.DoIpInformation
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., customer_version: _Optional[int] = ..., sensor_ethernet_configuration_information: _Optional[_Union[_sensor_ethernet_configuration_information_pb2.SensorEthernetConfigurationInformation, _Mapping]] = ..., diagnostics_ethernet_configuration_information: _Optional[_Union[_diagnostics_ethernet_configuration_information_pb2.DiagnosticsEthernetConfigurationInformation, _Mapping]] = ..., sensor_mac_address: _Optional[int] = ..., doip_information: _Optional[_Union[_do_ip_information_pb2.DoIpInformation, _Mapping]] = ...) -> None: ...
