from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RxmSVSI_SV(_message.Message):
    __slots__ = ("svid", "svFlag", "azim", "elev", "age")
    SVID_FIELD_NUMBER: _ClassVar[int]
    SVFLAG_FIELD_NUMBER: _ClassVar[int]
    AZIM_FIELD_NUMBER: _ClassVar[int]
    ELEV_FIELD_NUMBER: _ClassVar[int]
    AGE_FIELD_NUMBER: _ClassVar[int]
    svid: int
    svFlag: int
    azim: int
    elev: int
    age: int
    def __init__(self, svid: _Optional[int] = ..., svFlag: _Optional[int] = ..., azim: _Optional[int] = ..., elev: _Optional[int] = ..., age: _Optional[int] = ...) -> None: ...
