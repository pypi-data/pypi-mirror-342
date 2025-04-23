from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ListLabelsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListLabelsResponse(_message.Message):
    __slots__ = ("ids", "labels")
    IDS_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[int]
    labels: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, ids: _Optional[_Iterable[int]] = ..., labels: _Optional[_Iterable[str]] = ...) -> None: ...
