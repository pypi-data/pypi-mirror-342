from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class NavDGPSSV(_message.Message):
    __slots__ = ("svid", "flags", "age_c", "prc", "prrc")
    SVID_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    AGE_C_FIELD_NUMBER: _ClassVar[int]
    PRC_FIELD_NUMBER: _ClassVar[int]
    PRRC_FIELD_NUMBER: _ClassVar[int]
    svid: int
    flags: int
    age_c: int
    prc: float
    prrc: float
    def __init__(self, svid: _Optional[int] = ..., flags: _Optional[int] = ..., age_c: _Optional[int] = ..., prc: _Optional[float] = ..., prrc: _Optional[float] = ...) -> None: ...
