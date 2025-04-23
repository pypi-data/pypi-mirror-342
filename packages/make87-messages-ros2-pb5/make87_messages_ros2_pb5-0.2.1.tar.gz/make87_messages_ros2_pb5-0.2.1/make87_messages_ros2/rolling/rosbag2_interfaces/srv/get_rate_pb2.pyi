from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GetRateRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetRateResponse(_message.Message):
    __slots__ = ("rate",)
    RATE_FIELD_NUMBER: _ClassVar[int]
    rate: float
    def __init__(self, rate: _Optional[float] = ...) -> None: ...
