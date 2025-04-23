from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ObjectHypothesis(_message.Message):
    __slots__ = ("header", "class_id", "score")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CLASS_ID_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    class_id: str
    score: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., class_id: _Optional[str] = ..., score: _Optional[float] = ...) -> None: ...
