from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class BumperEvent(_message.Message):
    __slots__ = ("bumper", "state")
    BUMPER_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    bumper: int
    state: int
    def __init__(self, bumper: _Optional[int] = ..., state: _Optional[int] = ...) -> None: ...
