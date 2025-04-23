from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SaveGridRequest(_message.Message):
    __slots__ = ("file_name",)
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    file_name: str
    def __init__(self, file_name: _Optional[str] = ...) -> None: ...

class SaveGridResponse(_message.Message):
    __slots__ = ("map_size_bytes", "status")
    MAP_SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    map_size_bytes: float
    status: bool
    def __init__(self, map_size_bytes: _Optional[float] = ..., status: bool = ...) -> None: ...
