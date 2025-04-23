from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MapLoadRequest(_message.Message):
    __slots__ = ("header", "map_path")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MAP_PATH_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    map_path: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., map_path: _Optional[str] = ...) -> None: ...

class MapLoadResponse(_message.Message):
    __slots__ = ("header", "success", "error_message")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    error_message: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., error_message: _Optional[str] = ...) -> None: ...
