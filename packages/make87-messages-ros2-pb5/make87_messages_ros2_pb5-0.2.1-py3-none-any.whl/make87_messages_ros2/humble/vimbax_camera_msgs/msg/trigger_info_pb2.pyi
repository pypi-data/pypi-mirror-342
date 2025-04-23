from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TriggerInfo(_message.Message):
    __slots__ = ("header", "selector", "mode", "source")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    selector: str
    mode: str
    source: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., selector: _Optional[str] = ..., mode: _Optional[str] = ..., source: _Optional[str] = ...) -> None: ...
