from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class FileEntry(_message.Message):
    __slots__ = ("name", "type", "size")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    name: str
    type: int
    size: int
    def __init__(self, name: _Optional[str] = ..., type: _Optional[int] = ..., size: _Optional[int] = ...) -> None: ...
