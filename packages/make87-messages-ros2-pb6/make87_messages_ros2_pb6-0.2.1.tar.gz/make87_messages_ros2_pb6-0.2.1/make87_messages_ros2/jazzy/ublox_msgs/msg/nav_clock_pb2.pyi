from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class NavCLOCK(_message.Message):
    __slots__ = ("i_tow", "clk_b", "clk_d", "t_acc", "f_acc")
    I_TOW_FIELD_NUMBER: _ClassVar[int]
    CLK_B_FIELD_NUMBER: _ClassVar[int]
    CLK_D_FIELD_NUMBER: _ClassVar[int]
    T_ACC_FIELD_NUMBER: _ClassVar[int]
    F_ACC_FIELD_NUMBER: _ClassVar[int]
    i_tow: int
    clk_b: int
    clk_d: int
    t_acc: int
    f_acc: int
    def __init__(self, i_tow: _Optional[int] = ..., clk_b: _Optional[int] = ..., clk_d: _Optional[int] = ..., t_acc: _Optional[int] = ..., f_acc: _Optional[int] = ...) -> None: ...
