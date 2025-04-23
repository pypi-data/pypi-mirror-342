from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SetAnalogOutputRequest(_message.Message):
    __slots__ = ("index", "voltage")
    INDEX_FIELD_NUMBER: _ClassVar[int]
    VOLTAGE_FIELD_NUMBER: _ClassVar[int]
    index: int
    voltage: float
    def __init__(self, index: _Optional[int] = ..., voltage: _Optional[float] = ...) -> None: ...

class SetAnalogOutputResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
