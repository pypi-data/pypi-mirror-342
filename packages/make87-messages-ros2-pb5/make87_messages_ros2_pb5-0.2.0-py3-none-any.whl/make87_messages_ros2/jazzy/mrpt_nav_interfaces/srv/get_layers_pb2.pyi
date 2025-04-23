from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GetLayersRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetLayersResponse(_message.Message):
    __slots__ = ("layers",)
    LAYERS_FIELD_NUMBER: _ClassVar[int]
    layers: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, layers: _Optional[_Iterable[str]] = ...) -> None: ...
