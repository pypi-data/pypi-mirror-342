from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.off_highway_premium_radar_sample_msgs.msg import interference_indicator_pb2 as _interference_indicator_pb2
from make87_messages_ros2.humble.off_highway_premium_radar_sample_msgs.msg import misalignment_packet_pb2 as _misalignment_packet_pb2
from make87_messages_ros2.humble.off_highway_premium_radar_sample_msgs.msg import sensor_field_of_view_pb2 as _sensor_field_of_view_pb2
from make87_messages_ros2.humble.off_highway_premium_radar_sample_msgs.msg import sensor_modulation_performance_pb2 as _sensor_modulation_performance_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LocationAttributesPacket(_message.Message):
    __slots__ = ("header", "sensor_modulation_performance", "misalignment", "interference_indicator", "sensor_field_of_view")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SENSOR_MODULATION_PERFORMANCE_FIELD_NUMBER: _ClassVar[int]
    MISALIGNMENT_FIELD_NUMBER: _ClassVar[int]
    INTERFERENCE_INDICATOR_FIELD_NUMBER: _ClassVar[int]
    SENSOR_FIELD_OF_VIEW_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    sensor_modulation_performance: _sensor_modulation_performance_pb2.SensorModulationPerformance
    misalignment: _misalignment_packet_pb2.MisalignmentPacket
    interference_indicator: _interference_indicator_pb2.InterferenceIndicator
    sensor_field_of_view: _sensor_field_of_view_pb2.SensorFieldOfView
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., sensor_modulation_performance: _Optional[_Union[_sensor_modulation_performance_pb2.SensorModulationPerformance, _Mapping]] = ..., misalignment: _Optional[_Union[_misalignment_packet_pb2.MisalignmentPacket, _Mapping]] = ..., interference_indicator: _Optional[_Union[_interference_indicator_pb2.InterferenceIndicator, _Mapping]] = ..., sensor_field_of_view: _Optional[_Union[_sensor_field_of_view_pb2.SensorFieldOfView, _Mapping]] = ...) -> None: ...
