from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EcuInfo(_message.Message):
    __slots__ = ("header", "ros2_header", "name", "version", "mac_addr", "config_hash", "config_count_modified", "config_count_configured", "config_nvm_blank", "config_nvm_write_pending", "build_date", "license_date", "control_licensed", "log_filename", "log_filesystem_present", "log_fault")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    MAC_ADDR_FIELD_NUMBER: _ClassVar[int]
    CONFIG_HASH_FIELD_NUMBER: _ClassVar[int]
    CONFIG_COUNT_MODIFIED_FIELD_NUMBER: _ClassVar[int]
    CONFIG_COUNT_CONFIGURED_FIELD_NUMBER: _ClassVar[int]
    CONFIG_NVM_BLANK_FIELD_NUMBER: _ClassVar[int]
    CONFIG_NVM_WRITE_PENDING_FIELD_NUMBER: _ClassVar[int]
    BUILD_DATE_FIELD_NUMBER: _ClassVar[int]
    LICENSE_DATE_FIELD_NUMBER: _ClassVar[int]
    CONTROL_LICENSED_FIELD_NUMBER: _ClassVar[int]
    LOG_FILENAME_FIELD_NUMBER: _ClassVar[int]
    LOG_FILESYSTEM_PRESENT_FIELD_NUMBER: _ClassVar[int]
    LOG_FAULT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    name: str
    version: str
    mac_addr: str
    config_hash: str
    config_count_modified: int
    config_count_configured: int
    config_nvm_blank: bool
    config_nvm_write_pending: bool
    build_date: str
    license_date: str
    control_licensed: bool
    log_filename: str
    log_filesystem_present: bool
    log_fault: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., name: _Optional[str] = ..., version: _Optional[str] = ..., mac_addr: _Optional[str] = ..., config_hash: _Optional[str] = ..., config_count_modified: _Optional[int] = ..., config_count_configured: _Optional[int] = ..., config_nvm_blank: bool = ..., config_nvm_write_pending: bool = ..., build_date: _Optional[str] = ..., license_date: _Optional[str] = ..., control_licensed: bool = ..., log_filename: _Optional[str] = ..., log_filesystem_present: bool = ..., log_fault: bool = ...) -> None: ...
