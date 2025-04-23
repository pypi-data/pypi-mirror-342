from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GetDomainConstantsRequest(_message.Message):
    __slots__ = ("type",)
    TYPE_FIELD_NUMBER: _ClassVar[int]
    type: str
    def __init__(self, type: _Optional[str] = ...) -> None: ...

class GetDomainConstantsResponse(_message.Message):
    __slots__ = ("success", "constants", "error_info")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    CONSTANTS_FIELD_NUMBER: _ClassVar[int]
    ERROR_INFO_FIELD_NUMBER: _ClassVar[int]
    success: bool
    constants: _containers.RepeatedScalarFieldContainer[str]
    error_info: str
    def __init__(self, success: bool = ..., constants: _Optional[_Iterable[str]] = ..., error_info: _Optional[str] = ...) -> None: ...
