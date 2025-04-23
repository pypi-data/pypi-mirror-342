from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FieldInformation(_message.Message):
    __slots__ = ("header", "field_id", "field_set_id", "field_result", "eval_method", "field_active")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FIELD_ID_FIELD_NUMBER: _ClassVar[int]
    FIELD_SET_ID_FIELD_NUMBER: _ClassVar[int]
    FIELD_RESULT_FIELD_NUMBER: _ClassVar[int]
    EVAL_METHOD_FIELD_NUMBER: _ClassVar[int]
    FIELD_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    field_id: int
    field_set_id: int
    field_result: int
    eval_method: int
    field_active: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., field_id: _Optional[int] = ..., field_set_id: _Optional[int] = ..., field_result: _Optional[int] = ..., eval_method: _Optional[int] = ..., field_active: _Optional[int] = ...) -> None: ...
