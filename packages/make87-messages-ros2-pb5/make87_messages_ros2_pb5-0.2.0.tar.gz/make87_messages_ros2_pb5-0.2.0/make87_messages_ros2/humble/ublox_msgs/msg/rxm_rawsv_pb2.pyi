from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RxmRAWSV(_message.Message):
    __slots__ = ("header", "cp_mes", "pr_mes", "do_mes", "sv", "mes_qi", "cno", "lli")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CP_MES_FIELD_NUMBER: _ClassVar[int]
    PR_MES_FIELD_NUMBER: _ClassVar[int]
    DO_MES_FIELD_NUMBER: _ClassVar[int]
    SV_FIELD_NUMBER: _ClassVar[int]
    MES_QI_FIELD_NUMBER: _ClassVar[int]
    CNO_FIELD_NUMBER: _ClassVar[int]
    LLI_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    cp_mes: float
    pr_mes: float
    do_mes: float
    sv: int
    mes_qi: int
    cno: int
    lli: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., cp_mes: _Optional[float] = ..., pr_mes: _Optional[float] = ..., do_mes: _Optional[float] = ..., sv: _Optional[int] = ..., mes_qi: _Optional[int] = ..., cno: _Optional[int] = ..., lli: _Optional[int] = ...) -> None: ...
