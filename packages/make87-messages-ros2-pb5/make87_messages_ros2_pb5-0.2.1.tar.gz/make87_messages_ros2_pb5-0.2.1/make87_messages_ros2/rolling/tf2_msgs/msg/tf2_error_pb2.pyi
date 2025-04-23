from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class TF2Error(_message.Message):
    __slots__ = ("error", "error_string")
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ERROR_STRING_FIELD_NUMBER: _ClassVar[int]
    error: int
    error_string: str
    def __init__(self, error: _Optional[int] = ..., error_string: _Optional[str] = ...) -> None: ...
