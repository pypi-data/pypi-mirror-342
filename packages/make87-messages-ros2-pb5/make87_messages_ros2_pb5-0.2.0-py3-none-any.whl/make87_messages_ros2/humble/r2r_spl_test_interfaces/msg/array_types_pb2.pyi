from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ArrayTypes(_message.Message):
    __slots__ = ("header", "data_int8_static", "data_bool_static", "data_int8_unbounded_dynamic", "data_bool_unbounded_dynamic", "data_int8_bounded_dynamic", "data_bool_bounded_dynamic", "data_string", "data_string_bounded", "data_wstring", "data_wstring_bounded")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DATA_INT8_STATIC_FIELD_NUMBER: _ClassVar[int]
    DATA_BOOL_STATIC_FIELD_NUMBER: _ClassVar[int]
    DATA_INT8_UNBOUNDED_DYNAMIC_FIELD_NUMBER: _ClassVar[int]
    DATA_BOOL_UNBOUNDED_DYNAMIC_FIELD_NUMBER: _ClassVar[int]
    DATA_INT8_BOUNDED_DYNAMIC_FIELD_NUMBER: _ClassVar[int]
    DATA_BOOL_BOUNDED_DYNAMIC_FIELD_NUMBER: _ClassVar[int]
    DATA_STRING_FIELD_NUMBER: _ClassVar[int]
    DATA_STRING_BOUNDED_FIELD_NUMBER: _ClassVar[int]
    DATA_WSTRING_FIELD_NUMBER: _ClassVar[int]
    DATA_WSTRING_BOUNDED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    data_int8_static: _containers.RepeatedScalarFieldContainer[int]
    data_bool_static: _containers.RepeatedScalarFieldContainer[bool]
    data_int8_unbounded_dynamic: _containers.RepeatedScalarFieldContainer[int]
    data_bool_unbounded_dynamic: _containers.RepeatedScalarFieldContainer[bool]
    data_int8_bounded_dynamic: _containers.RepeatedScalarFieldContainer[int]
    data_bool_bounded_dynamic: _containers.RepeatedScalarFieldContainer[bool]
    data_string: str
    data_string_bounded: str
    data_wstring: str
    data_wstring_bounded: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., data_int8_static: _Optional[_Iterable[int]] = ..., data_bool_static: _Optional[_Iterable[bool]] = ..., data_int8_unbounded_dynamic: _Optional[_Iterable[int]] = ..., data_bool_unbounded_dynamic: _Optional[_Iterable[bool]] = ..., data_int8_bounded_dynamic: _Optional[_Iterable[int]] = ..., data_bool_bounded_dynamic: _Optional[_Iterable[bool]] = ..., data_string: _Optional[str] = ..., data_string_bounded: _Optional[str] = ..., data_wstring: _Optional[str] = ..., data_wstring_bounded: _Optional[str] = ...) -> None: ...
