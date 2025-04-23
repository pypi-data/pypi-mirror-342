from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ForceResistance(_message.Message):
    __slots__ = ("name", "px", "py", "pz", "fx", "fy", "fz")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PX_FIELD_NUMBER: _ClassVar[int]
    PY_FIELD_NUMBER: _ClassVar[int]
    PZ_FIELD_NUMBER: _ClassVar[int]
    FX_FIELD_NUMBER: _ClassVar[int]
    FY_FIELD_NUMBER: _ClassVar[int]
    FZ_FIELD_NUMBER: _ClassVar[int]
    name: str
    px: float
    py: float
    pz: float
    fx: float
    fy: float
    fz: float
    def __init__(self, name: _Optional[str] = ..., px: _Optional[float] = ..., py: _Optional[float] = ..., pz: _Optional[float] = ..., fx: _Optional[float] = ..., fy: _Optional[float] = ..., fz: _Optional[float] = ...) -> None: ...
