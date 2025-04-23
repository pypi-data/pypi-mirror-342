from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ObjectType(_message.Message):
    __slots__ = ("key", "db")
    KEY_FIELD_NUMBER: _ClassVar[int]
    DB_FIELD_NUMBER: _ClassVar[int]
    key: str
    db: str
    def __init__(self, key: _Optional[str] = ..., db: _Optional[str] = ...) -> None: ...
