from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class TrkStat(_message.Message):
    __slots__ = ("pr_valid", "cp_valid", "half_cyc", "sub_half_cyc")
    PR_VALID_FIELD_NUMBER: _ClassVar[int]
    CP_VALID_FIELD_NUMBER: _ClassVar[int]
    HALF_CYC_FIELD_NUMBER: _ClassVar[int]
    SUB_HALF_CYC_FIELD_NUMBER: _ClassVar[int]
    pr_valid: bool
    cp_valid: bool
    half_cyc: bool
    sub_half_cyc: bool
    def __init__(self, pr_valid: bool = ..., cp_valid: bool = ..., half_cyc: bool = ..., sub_half_cyc: bool = ...) -> None: ...
