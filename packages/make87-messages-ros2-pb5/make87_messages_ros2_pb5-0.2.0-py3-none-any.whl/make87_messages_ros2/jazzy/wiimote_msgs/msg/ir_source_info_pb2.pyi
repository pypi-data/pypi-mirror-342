from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class IrSourceInfo(_message.Message):
    __slots__ = ("x", "y", "ir_size")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    IR_SIZE_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    ir_size: int
    def __init__(self, x: _Optional[float] = ..., y: _Optional[float] = ..., ir_size: _Optional[int] = ...) -> None: ...
