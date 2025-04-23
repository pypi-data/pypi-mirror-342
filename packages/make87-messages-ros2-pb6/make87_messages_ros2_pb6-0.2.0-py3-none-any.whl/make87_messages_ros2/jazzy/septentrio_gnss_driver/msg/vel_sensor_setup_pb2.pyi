from make87_messages_ros2.jazzy.septentrio_gnss_driver.msg import block_header_pb2 as _block_header_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VelSensorSetup(_message.Message):
    __slots__ = ("header", "block_header", "port", "lever_arm_x", "lever_arm_y", "lever_arm_z")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BLOCK_HEADER_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    LEVER_ARM_X_FIELD_NUMBER: _ClassVar[int]
    LEVER_ARM_Y_FIELD_NUMBER: _ClassVar[int]
    LEVER_ARM_Z_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    block_header: _block_header_pb2.BlockHeader
    port: int
    lever_arm_x: float
    lever_arm_y: float
    lever_arm_z: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., block_header: _Optional[_Union[_block_header_pb2.BlockHeader, _Mapping]] = ..., port: _Optional[int] = ..., lever_arm_x: _Optional[float] = ..., lever_arm_y: _Optional[float] = ..., lever_arm_z: _Optional[float] = ...) -> None: ...
