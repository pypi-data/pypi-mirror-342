from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MessageIntervalRequest(_message.Message):
    __slots__ = ("header", "message_id", "message_rate")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_RATE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    message_id: int
    message_rate: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., message_id: _Optional[int] = ..., message_rate: _Optional[float] = ...) -> None: ...

class MessageIntervalResponse(_message.Message):
    __slots__ = ("header", "success")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ...) -> None: ...
