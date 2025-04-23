from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AudioInfo(_message.Message):
    __slots__ = ("channels", "sample_rate", "sample_format", "bitrate", "coding_format")
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_RATE_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_FORMAT_FIELD_NUMBER: _ClassVar[int]
    BITRATE_FIELD_NUMBER: _ClassVar[int]
    CODING_FORMAT_FIELD_NUMBER: _ClassVar[int]
    channels: int
    sample_rate: int
    sample_format: str
    bitrate: int
    coding_format: str
    def __init__(self, channels: _Optional[int] = ..., sample_rate: _Optional[int] = ..., sample_format: _Optional[str] = ..., bitrate: _Optional[int] = ..., coding_format: _Optional[str] = ...) -> None: ...
