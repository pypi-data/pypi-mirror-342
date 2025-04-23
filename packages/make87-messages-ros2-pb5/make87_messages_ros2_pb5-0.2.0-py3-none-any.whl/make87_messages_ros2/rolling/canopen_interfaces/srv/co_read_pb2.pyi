from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class COReadRequest(_message.Message):
    __slots__ = ("index", "subindex")
    INDEX_FIELD_NUMBER: _ClassVar[int]
    SUBINDEX_FIELD_NUMBER: _ClassVar[int]
    index: int
    subindex: int
    def __init__(self, index: _Optional[int] = ..., subindex: _Optional[int] = ...) -> None: ...

class COReadResponse(_message.Message):
    __slots__ = ("success", "data")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    success: bool
    data: int
    def __init__(self, success: bool = ..., data: _Optional[int] = ...) -> None: ...
