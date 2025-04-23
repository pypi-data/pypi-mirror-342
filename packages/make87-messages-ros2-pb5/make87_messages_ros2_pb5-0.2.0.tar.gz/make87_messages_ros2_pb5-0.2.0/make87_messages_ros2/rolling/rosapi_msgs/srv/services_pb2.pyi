from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ServicesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ServicesResponse(_message.Message):
    __slots__ = ("services",)
    SERVICES_FIELD_NUMBER: _ClassVar[int]
    services: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, services: _Optional[_Iterable[str]] = ...) -> None: ...
