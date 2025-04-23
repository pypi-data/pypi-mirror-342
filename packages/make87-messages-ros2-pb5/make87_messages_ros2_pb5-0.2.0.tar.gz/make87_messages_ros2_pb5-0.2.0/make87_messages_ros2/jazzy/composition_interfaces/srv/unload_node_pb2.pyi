from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class UnloadNodeRequest(_message.Message):
    __slots__ = ("unique_id",)
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    def __init__(self, unique_id: _Optional[int] = ...) -> None: ...

class UnloadNodeResponse(_message.Message):
    __slots__ = ("success", "error_message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    error_message: str
    def __init__(self, success: bool = ..., error_message: _Optional[str] = ...) -> None: ...
