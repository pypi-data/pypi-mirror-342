from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SetPidGainsRequest(_message.Message):
    __slots__ = ("p", "i", "d", "i_clamp", "antiwindup")
    P_FIELD_NUMBER: _ClassVar[int]
    I_FIELD_NUMBER: _ClassVar[int]
    D_FIELD_NUMBER: _ClassVar[int]
    I_CLAMP_FIELD_NUMBER: _ClassVar[int]
    ANTIWINDUP_FIELD_NUMBER: _ClassVar[int]
    p: float
    i: float
    d: float
    i_clamp: float
    antiwindup: bool
    def __init__(self, p: _Optional[float] = ..., i: _Optional[float] = ..., d: _Optional[float] = ..., i_clamp: _Optional[float] = ..., antiwindup: bool = ...) -> None: ...

class SetPidGainsResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
