from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ContourPointSigma(_message.Message):
    __slots__ = ("x", "y", "x_sigma", "y_sigma")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    X_SIGMA_FIELD_NUMBER: _ClassVar[int]
    Y_SIGMA_FIELD_NUMBER: _ClassVar[int]
    x: int
    y: int
    x_sigma: int
    y_sigma: int
    def __init__(self, x: _Optional[int] = ..., y: _Optional[int] = ..., x_sigma: _Optional[int] = ..., y_sigma: _Optional[int] = ...) -> None: ...
