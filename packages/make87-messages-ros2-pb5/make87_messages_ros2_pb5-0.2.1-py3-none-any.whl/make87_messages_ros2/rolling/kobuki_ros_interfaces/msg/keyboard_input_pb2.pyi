from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class KeyboardInput(_message.Message):
    __slots__ = ("pressed_key",)
    PRESSED_KEY_FIELD_NUMBER: _ClassVar[int]
    pressed_key: int
    def __init__(self, pressed_key: _Optional[int] = ...) -> None: ...
