from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Intent(_message.Message):
    __slots__ = ("header", "intent", "data", "source", "modality", "priority", "confidence")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    INTENT_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    MODALITY_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    intent: str
    data: str
    source: str
    modality: str
    priority: int
    confidence: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., intent: _Optional[str] = ..., data: _Optional[str] = ..., source: _Optional[str] = ..., modality: _Optional[str] = ..., priority: _Optional[int] = ..., confidence: _Optional[float] = ...) -> None: ...
