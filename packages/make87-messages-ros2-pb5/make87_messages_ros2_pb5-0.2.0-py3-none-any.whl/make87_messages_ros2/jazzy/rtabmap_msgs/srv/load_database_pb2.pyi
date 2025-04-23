from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class LoadDatabaseRequest(_message.Message):
    __slots__ = ("database_path", "clear")
    DATABASE_PATH_FIELD_NUMBER: _ClassVar[int]
    CLEAR_FIELD_NUMBER: _ClassVar[int]
    database_path: str
    clear: bool
    def __init__(self, database_path: _Optional[str] = ..., clear: bool = ...) -> None: ...

class LoadDatabaseResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
