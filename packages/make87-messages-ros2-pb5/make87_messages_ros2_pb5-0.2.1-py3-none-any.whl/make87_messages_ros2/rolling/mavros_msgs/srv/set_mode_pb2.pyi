from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SetModeRequest(_message.Message):
    __slots__ = ("base_mode", "custom_mode")
    BASE_MODE_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_MODE_FIELD_NUMBER: _ClassVar[int]
    base_mode: int
    custom_mode: str
    def __init__(self, base_mode: _Optional[int] = ..., custom_mode: _Optional[str] = ...) -> None: ...

class SetModeResponse(_message.Message):
    __slots__ = ("mode_sent",)
    MODE_SENT_FIELD_NUMBER: _ClassVar[int]
    mode_sent: bool
    def __init__(self, mode_sent: bool = ...) -> None: ...
