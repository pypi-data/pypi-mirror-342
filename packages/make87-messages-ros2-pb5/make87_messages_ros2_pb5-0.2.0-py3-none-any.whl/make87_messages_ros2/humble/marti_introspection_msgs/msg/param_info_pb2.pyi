from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ParamInfo(_message.Message):
    __slots__ = ("header", "name", "resolved_name", "description", "group", "type", "dynamic", "default_int", "default_float", "default_double", "default_string", "default_bool", "max_value", "min_value")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    RESOLVED_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DYNAMIC_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_INT_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_FLOAT_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_DOUBLE_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_STRING_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_BOOL_FIELD_NUMBER: _ClassVar[int]
    MAX_VALUE_FIELD_NUMBER: _ClassVar[int]
    MIN_VALUE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    name: str
    resolved_name: str
    description: str
    group: str
    type: int
    dynamic: bool
    default_int: int
    default_float: float
    default_double: float
    default_string: str
    default_bool: bool
    max_value: float
    min_value: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., name: _Optional[str] = ..., resolved_name: _Optional[str] = ..., description: _Optional[str] = ..., group: _Optional[str] = ..., type: _Optional[int] = ..., dynamic: bool = ..., default_int: _Optional[int] = ..., default_float: _Optional[float] = ..., default_double: _Optional[float] = ..., default_string: _Optional[str] = ..., default_bool: bool = ..., max_value: _Optional[float] = ..., min_value: _Optional[float] = ...) -> None: ...
