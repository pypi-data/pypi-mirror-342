from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class MuxSelectRequest(_message.Message):
    __slots__ = ("topic",)
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    topic: str
    def __init__(self, topic: _Optional[str] = ...) -> None: ...

class MuxSelectResponse(_message.Message):
    __slots__ = ("prev_topic", "success")
    PREV_TOPIC_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    prev_topic: str
    success: bool
    def __init__(self, prev_topic: _Optional[str] = ..., success: bool = ...) -> None: ...
