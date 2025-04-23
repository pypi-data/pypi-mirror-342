from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CfgCFG(_message.Message):
    __slots__ = ("clear_mask", "save_mask", "load_mask", "device_mask")
    CLEAR_MASK_FIELD_NUMBER: _ClassVar[int]
    SAVE_MASK_FIELD_NUMBER: _ClassVar[int]
    LOAD_MASK_FIELD_NUMBER: _ClassVar[int]
    DEVICE_MASK_FIELD_NUMBER: _ClassVar[int]
    clear_mask: int
    save_mask: int
    load_mask: int
    device_mask: int
    def __init__(self, clear_mask: _Optional[int] = ..., save_mask: _Optional[int] = ..., load_mask: _Optional[int] = ..., device_mask: _Optional[int] = ...) -> None: ...
