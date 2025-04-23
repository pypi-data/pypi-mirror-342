from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AlertResponse(_message.Message):
    __slots__ = ("id", "response")
    ID_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    id: str
    response: str
    def __init__(self, id: _Optional[str] = ..., response: _Optional[str] = ...) -> None: ...
