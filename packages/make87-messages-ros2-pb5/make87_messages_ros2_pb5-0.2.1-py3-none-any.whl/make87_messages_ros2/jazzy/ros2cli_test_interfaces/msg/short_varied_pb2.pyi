from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ShortVaried(_message.Message):
    __slots__ = ("bool_value", "bool_values")
    BOOL_VALUE_FIELD_NUMBER: _ClassVar[int]
    BOOL_VALUES_FIELD_NUMBER: _ClassVar[int]
    bool_value: bool
    bool_values: _containers.RepeatedScalarFieldContainer[bool]
    def __init__(self, bool_value: bool = ..., bool_values: _Optional[_Iterable[bool]] = ...) -> None: ...
