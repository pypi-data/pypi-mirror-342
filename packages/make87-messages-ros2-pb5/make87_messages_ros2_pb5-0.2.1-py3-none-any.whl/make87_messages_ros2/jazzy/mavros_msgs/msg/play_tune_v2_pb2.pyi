from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PlayTuneV2(_message.Message):
    __slots__ = ("format", "tune")
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    TUNE_FIELD_NUMBER: _ClassVar[int]
    format: int
    tune: str
    def __init__(self, format: _Optional[int] = ..., tune: _Optional[str] = ...) -> None: ...
