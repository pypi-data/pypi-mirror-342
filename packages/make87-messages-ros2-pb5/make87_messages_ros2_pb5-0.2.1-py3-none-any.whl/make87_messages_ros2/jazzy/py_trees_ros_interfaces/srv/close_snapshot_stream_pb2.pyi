from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CloseSnapshotStreamRequest(_message.Message):
    __slots__ = ("topic_name",)
    TOPIC_NAME_FIELD_NUMBER: _ClassVar[int]
    topic_name: str
    def __init__(self, topic_name: _Optional[str] = ...) -> None: ...

class CloseSnapshotStreamResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: bool
    def __init__(self, result: bool = ...) -> None: ...
