from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.septentrio_gnss_driver.msg import block_header_pb2 as _block_header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ExtSensorMeas(_message.Message):
    __slots__ = ("header", "ros2_header", "block_header", "n", "sb_length", "source", "sensor_model", "type", "obs_info", "acceleration_x", "acceleration_y", "acceleration_z", "angular_rate_x", "angular_rate_y", "angular_rate_z", "velocity_x", "velocity_y", "velocity_z", "std_dev_x", "std_dev_y", "std_dev_z", "sensor_temperature", "zero_velocity_flag")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    BLOCK_HEADER_FIELD_NUMBER: _ClassVar[int]
    N_FIELD_NUMBER: _ClassVar[int]
    SB_LENGTH_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    SENSOR_MODEL_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    OBS_INFO_FIELD_NUMBER: _ClassVar[int]
    ACCELERATION_X_FIELD_NUMBER: _ClassVar[int]
    ACCELERATION_Y_FIELD_NUMBER: _ClassVar[int]
    ACCELERATION_Z_FIELD_NUMBER: _ClassVar[int]
    ANGULAR_RATE_X_FIELD_NUMBER: _ClassVar[int]
    ANGULAR_RATE_Y_FIELD_NUMBER: _ClassVar[int]
    ANGULAR_RATE_Z_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_X_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_Y_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_Z_FIELD_NUMBER: _ClassVar[int]
    STD_DEV_X_FIELD_NUMBER: _ClassVar[int]
    STD_DEV_Y_FIELD_NUMBER: _ClassVar[int]
    STD_DEV_Z_FIELD_NUMBER: _ClassVar[int]
    SENSOR_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    ZERO_VELOCITY_FLAG_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    block_header: _block_header_pb2.BlockHeader
    n: int
    sb_length: int
    source: _containers.RepeatedScalarFieldContainer[int]
    sensor_model: _containers.RepeatedScalarFieldContainer[int]
    type: _containers.RepeatedScalarFieldContainer[int]
    obs_info: _containers.RepeatedScalarFieldContainer[int]
    acceleration_x: float
    acceleration_y: float
    acceleration_z: float
    angular_rate_x: float
    angular_rate_y: float
    angular_rate_z: float
    velocity_x: float
    velocity_y: float
    velocity_z: float
    std_dev_x: float
    std_dev_y: float
    std_dev_z: float
    sensor_temperature: float
    zero_velocity_flag: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., block_header: _Optional[_Union[_block_header_pb2.BlockHeader, _Mapping]] = ..., n: _Optional[int] = ..., sb_length: _Optional[int] = ..., source: _Optional[_Iterable[int]] = ..., sensor_model: _Optional[_Iterable[int]] = ..., type: _Optional[_Iterable[int]] = ..., obs_info: _Optional[_Iterable[int]] = ..., acceleration_x: _Optional[float] = ..., acceleration_y: _Optional[float] = ..., acceleration_z: _Optional[float] = ..., angular_rate_x: _Optional[float] = ..., angular_rate_y: _Optional[float] = ..., angular_rate_z: _Optional[float] = ..., velocity_x: _Optional[float] = ..., velocity_y: _Optional[float] = ..., velocity_z: _Optional[float] = ..., std_dev_x: _Optional[float] = ..., std_dev_y: _Optional[float] = ..., std_dev_z: _Optional[float] = ..., sensor_temperature: _Optional[float] = ..., zero_velocity_flag: _Optional[float] = ...) -> None: ...
