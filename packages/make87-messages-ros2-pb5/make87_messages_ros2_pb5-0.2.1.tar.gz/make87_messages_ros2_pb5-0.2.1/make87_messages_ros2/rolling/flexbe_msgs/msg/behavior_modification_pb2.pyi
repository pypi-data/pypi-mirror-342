from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class BehaviorModification(_message.Message):
    __slots__ = ("index_begin", "index_end", "new_content")
    INDEX_BEGIN_FIELD_NUMBER: _ClassVar[int]
    INDEX_END_FIELD_NUMBER: _ClassVar[int]
    NEW_CONTENT_FIELD_NUMBER: _ClassVar[int]
    index_begin: int
    index_end: int
    new_content: str
    def __init__(self, index_begin: _Optional[int] = ..., index_end: _Optional[int] = ..., new_content: _Optional[str] = ...) -> None: ...
