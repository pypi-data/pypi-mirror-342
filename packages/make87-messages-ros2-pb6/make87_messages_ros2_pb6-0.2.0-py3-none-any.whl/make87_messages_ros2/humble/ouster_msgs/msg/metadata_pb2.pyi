from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Metadata(_message.Message):
    __slots__ = ("header", "hostname", "lidar_mode", "timestamp_mode", "beam_azimuth_angles", "beam_altitude_angles", "imu_to_sensor_transform", "lidar_to_sensor_transform", "serial_no", "firmware_rev", "imu_port", "lidar_port")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    LIDAR_MODE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_MODE_FIELD_NUMBER: _ClassVar[int]
    BEAM_AZIMUTH_ANGLES_FIELD_NUMBER: _ClassVar[int]
    BEAM_ALTITUDE_ANGLES_FIELD_NUMBER: _ClassVar[int]
    IMU_TO_SENSOR_TRANSFORM_FIELD_NUMBER: _ClassVar[int]
    LIDAR_TO_SENSOR_TRANSFORM_FIELD_NUMBER: _ClassVar[int]
    SERIAL_NO_FIELD_NUMBER: _ClassVar[int]
    FIRMWARE_REV_FIELD_NUMBER: _ClassVar[int]
    IMU_PORT_FIELD_NUMBER: _ClassVar[int]
    LIDAR_PORT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    hostname: str
    lidar_mode: str
    timestamp_mode: str
    beam_azimuth_angles: _containers.RepeatedScalarFieldContainer[float]
    beam_altitude_angles: _containers.RepeatedScalarFieldContainer[float]
    imu_to_sensor_transform: _containers.RepeatedScalarFieldContainer[float]
    lidar_to_sensor_transform: _containers.RepeatedScalarFieldContainer[float]
    serial_no: str
    firmware_rev: str
    imu_port: int
    lidar_port: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., hostname: _Optional[str] = ..., lidar_mode: _Optional[str] = ..., timestamp_mode: _Optional[str] = ..., beam_azimuth_angles: _Optional[_Iterable[float]] = ..., beam_altitude_angles: _Optional[_Iterable[float]] = ..., imu_to_sensor_transform: _Optional[_Iterable[float]] = ..., lidar_to_sensor_transform: _Optional[_Iterable[float]] = ..., serial_no: _Optional[str] = ..., firmware_rev: _Optional[str] = ..., imu_port: _Optional[int] = ..., lidar_port: _Optional[int] = ...) -> None: ...
