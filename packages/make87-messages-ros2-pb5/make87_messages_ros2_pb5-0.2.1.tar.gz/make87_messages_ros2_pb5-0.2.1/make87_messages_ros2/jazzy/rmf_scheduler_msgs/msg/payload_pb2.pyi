from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Payload(_message.Message):
    __slots__ = ("type", "topic", "message_type", "data")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    type: int
    topic: str
    message_type: str
    data: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, type: _Optional[int] = ..., topic: _Optional[str] = ..., message_type: _Optional[str] = ..., data: _Optional[_Iterable[int]] = ...) -> None: ...
