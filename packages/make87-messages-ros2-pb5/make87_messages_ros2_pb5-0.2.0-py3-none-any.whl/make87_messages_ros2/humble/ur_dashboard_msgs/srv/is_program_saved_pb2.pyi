from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IsProgramSavedRequest(_message.Message):
    __slots__ = ("header",)
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...

class IsProgramSavedResponse(_message.Message):
    __slots__ = ("header", "answer", "program_name", "program_saved", "success")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ANSWER_FIELD_NUMBER: _ClassVar[int]
    PROGRAM_NAME_FIELD_NUMBER: _ClassVar[int]
    PROGRAM_SAVED_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    answer: str
    program_name: str
    program_saved: bool
    success: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., answer: _Optional[str] = ..., program_name: _Optional[str] = ..., program_saved: bool = ..., success: bool = ...) -> None: ...
