from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class FileWriteRequest(_message.Message):
    __slots__ = ("file_path", "offset", "data")
    FILE_PATH_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    file_path: str
    offset: int
    data: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, file_path: _Optional[str] = ..., offset: _Optional[int] = ..., data: _Optional[_Iterable[int]] = ...) -> None: ...

class FileWriteResponse(_message.Message):
    __slots__ = ("success", "r_errno")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    R_ERRNO_FIELD_NUMBER: _ClassVar[int]
    success: bool
    r_errno: int
    def __init__(self, success: bool = ..., r_errno: _Optional[int] = ...) -> None: ...
