from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EStopRequest(_message.Message):
    __slots__ = ("header", "e_stop_on")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    E_STOP_ON_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    e_stop_on: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., e_stop_on: bool = ...) -> None: ...

class EStopResponse(_message.Message):
    __slots__ = ("header", "success", "message")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    message: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., message: _Optional[str] = ...) -> None: ...
