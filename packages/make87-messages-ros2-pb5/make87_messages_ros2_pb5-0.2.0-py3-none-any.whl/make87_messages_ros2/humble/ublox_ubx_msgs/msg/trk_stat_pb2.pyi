from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TrkStat(_message.Message):
    __slots__ = ("header", "pr_valid", "cp_valid", "half_cyc", "sub_half_cyc")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PR_VALID_FIELD_NUMBER: _ClassVar[int]
    CP_VALID_FIELD_NUMBER: _ClassVar[int]
    HALF_CYC_FIELD_NUMBER: _ClassVar[int]
    SUB_HALF_CYC_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    pr_valid: bool
    cp_valid: bool
    half_cyc: bool
    sub_half_cyc: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., pr_valid: bool = ..., cp_valid: bool = ..., half_cyc: bool = ..., sub_half_cyc: bool = ...) -> None: ...
