from make87_messages_ros2.rolling.ublox_msgs.msg import cfg_gnss_block_pb2 as _cfg_gnss_block_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CfgGNSS(_message.Message):
    __slots__ = ("msg_ver", "num_trk_ch_hw", "num_trk_ch_use", "num_config_blocks", "blocks")
    MSG_VER_FIELD_NUMBER: _ClassVar[int]
    NUM_TRK_CH_HW_FIELD_NUMBER: _ClassVar[int]
    NUM_TRK_CH_USE_FIELD_NUMBER: _ClassVar[int]
    NUM_CONFIG_BLOCKS_FIELD_NUMBER: _ClassVar[int]
    BLOCKS_FIELD_NUMBER: _ClassVar[int]
    msg_ver: int
    num_trk_ch_hw: int
    num_trk_ch_use: int
    num_config_blocks: int
    blocks: _containers.RepeatedCompositeFieldContainer[_cfg_gnss_block_pb2.CfgGNSSBlock]
    def __init__(self, msg_ver: _Optional[int] = ..., num_trk_ch_hw: _Optional[int] = ..., num_trk_ch_use: _Optional[int] = ..., num_config_blocks: _Optional[int] = ..., blocks: _Optional[_Iterable[_Union[_cfg_gnss_block_pb2.CfgGNSSBlock, _Mapping]]] = ...) -> None: ...
