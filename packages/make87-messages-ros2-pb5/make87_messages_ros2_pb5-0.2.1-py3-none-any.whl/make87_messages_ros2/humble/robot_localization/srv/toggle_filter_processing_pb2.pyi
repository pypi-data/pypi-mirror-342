from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ToggleFilterProcessingRequest(_message.Message):
    __slots__ = ("header", "on")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ON_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    on: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., on: bool = ...) -> None: ...

class ToggleFilterProcessingResponse(_message.Message):
    __slots__ = ("header", "status")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    status: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., status: bool = ...) -> None: ...
