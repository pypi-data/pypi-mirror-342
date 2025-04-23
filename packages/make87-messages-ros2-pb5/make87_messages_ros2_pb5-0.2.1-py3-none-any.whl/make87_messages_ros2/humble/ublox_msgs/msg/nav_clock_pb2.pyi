from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NavCLOCK(_message.Message):
    __slots__ = ("header", "i_tow", "clk_b", "clk_d", "t_acc", "f_acc")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    I_TOW_FIELD_NUMBER: _ClassVar[int]
    CLK_B_FIELD_NUMBER: _ClassVar[int]
    CLK_D_FIELD_NUMBER: _ClassVar[int]
    T_ACC_FIELD_NUMBER: _ClassVar[int]
    F_ACC_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    i_tow: int
    clk_b: int
    clk_d: int
    t_acc: int
    f_acc: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., i_tow: _Optional[int] = ..., clk_b: _Optional[int] = ..., clk_d: _Optional[int] = ..., t_acc: _Optional[int] = ..., f_acc: _Optional[int] = ...) -> None: ...
