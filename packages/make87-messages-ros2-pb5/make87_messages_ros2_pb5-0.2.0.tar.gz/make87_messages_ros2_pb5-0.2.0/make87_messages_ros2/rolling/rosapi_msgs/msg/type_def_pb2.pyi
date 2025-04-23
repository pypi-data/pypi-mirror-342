from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class TypeDef(_message.Message):
    __slots__ = ("type", "fieldnames", "fieldtypes", "fieldarraylen", "examples", "constnames", "constvalues")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    FIELDNAMES_FIELD_NUMBER: _ClassVar[int]
    FIELDTYPES_FIELD_NUMBER: _ClassVar[int]
    FIELDARRAYLEN_FIELD_NUMBER: _ClassVar[int]
    EXAMPLES_FIELD_NUMBER: _ClassVar[int]
    CONSTNAMES_FIELD_NUMBER: _ClassVar[int]
    CONSTVALUES_FIELD_NUMBER: _ClassVar[int]
    type: str
    fieldnames: _containers.RepeatedScalarFieldContainer[str]
    fieldtypes: _containers.RepeatedScalarFieldContainer[str]
    fieldarraylen: _containers.RepeatedScalarFieldContainer[int]
    examples: _containers.RepeatedScalarFieldContainer[str]
    constnames: _containers.RepeatedScalarFieldContainer[str]
    constvalues: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, type: _Optional[str] = ..., fieldnames: _Optional[_Iterable[str]] = ..., fieldtypes: _Optional[_Iterable[str]] = ..., fieldarraylen: _Optional[_Iterable[int]] = ..., examples: _Optional[_Iterable[str]] = ..., constnames: _Optional[_Iterable[str]] = ..., constvalues: _Optional[_Iterable[str]] = ...) -> None: ...
