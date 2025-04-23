from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class HardwareInterface(_message.Message):
    __slots__ = ("name", "is_available", "is_claimed")
    NAME_FIELD_NUMBER: _ClassVar[int]
    IS_AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    IS_CLAIMED_FIELD_NUMBER: _ClassVar[int]
    name: str
    is_available: bool
    is_claimed: bool
    def __init__(self, name: _Optional[str] = ..., is_available: bool = ..., is_claimed: bool = ...) -> None: ...
