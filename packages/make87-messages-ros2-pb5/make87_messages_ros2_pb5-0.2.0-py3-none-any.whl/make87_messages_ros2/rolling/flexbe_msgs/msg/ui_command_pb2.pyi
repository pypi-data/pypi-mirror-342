from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class UICommand(_message.Message):
    __slots__ = ("command", "key")
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    command: str
    key: str
    def __init__(self, command: _Optional[str] = ..., key: _Optional[str] = ...) -> None: ...
