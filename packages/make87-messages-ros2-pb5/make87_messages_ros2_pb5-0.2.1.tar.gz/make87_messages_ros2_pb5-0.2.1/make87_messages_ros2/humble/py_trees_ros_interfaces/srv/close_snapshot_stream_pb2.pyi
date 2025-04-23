from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CloseSnapshotStreamRequest(_message.Message):
    __slots__ = ("header", "topic_name")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TOPIC_NAME_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    topic_name: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., topic_name: _Optional[str] = ...) -> None: ...

class CloseSnapshotStreamResponse(_message.Message):
    __slots__ = ("header", "result")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    result: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., result: bool = ...) -> None: ...
