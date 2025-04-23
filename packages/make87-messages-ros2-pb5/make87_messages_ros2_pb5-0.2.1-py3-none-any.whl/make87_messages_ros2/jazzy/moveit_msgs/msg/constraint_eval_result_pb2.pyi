from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ConstraintEvalResult(_message.Message):
    __slots__ = ("result", "distance")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_FIELD_NUMBER: _ClassVar[int]
    result: bool
    distance: float
    def __init__(self, result: bool = ..., distance: _Optional[float] = ...) -> None: ...
