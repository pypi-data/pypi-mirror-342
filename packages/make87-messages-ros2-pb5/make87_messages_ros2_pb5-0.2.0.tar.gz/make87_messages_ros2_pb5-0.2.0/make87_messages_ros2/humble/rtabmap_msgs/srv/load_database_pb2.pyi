from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LoadDatabaseRequest(_message.Message):
    __slots__ = ("header", "database_path", "clear")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DATABASE_PATH_FIELD_NUMBER: _ClassVar[int]
    CLEAR_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    database_path: str
    clear: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., database_path: _Optional[str] = ..., clear: bool = ...) -> None: ...

class LoadDatabaseResponse(_message.Message):
    __slots__ = ("header",)
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...
