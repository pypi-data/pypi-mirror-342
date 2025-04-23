from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BasicTypes(_message.Message):
    __slots__ = ("header", "val_bool", "val_byte", "val_char", "val_float32", "val_float64", "val_int8", "val_uint8", "val_int16", "val_uint16", "val_int32", "val_uint32", "val_int64", "val_uint64")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    VAL_BOOL_FIELD_NUMBER: _ClassVar[int]
    VAL_BYTE_FIELD_NUMBER: _ClassVar[int]
    VAL_CHAR_FIELD_NUMBER: _ClassVar[int]
    VAL_FLOAT32_FIELD_NUMBER: _ClassVar[int]
    VAL_FLOAT64_FIELD_NUMBER: _ClassVar[int]
    VAL_INT8_FIELD_NUMBER: _ClassVar[int]
    VAL_UINT8_FIELD_NUMBER: _ClassVar[int]
    VAL_INT16_FIELD_NUMBER: _ClassVar[int]
    VAL_UINT16_FIELD_NUMBER: _ClassVar[int]
    VAL_INT32_FIELD_NUMBER: _ClassVar[int]
    VAL_UINT32_FIELD_NUMBER: _ClassVar[int]
    VAL_INT64_FIELD_NUMBER: _ClassVar[int]
    VAL_UINT64_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    val_bool: bool
    val_byte: int
    val_char: int
    val_float32: float
    val_float64: float
    val_int8: int
    val_uint8: int
    val_int16: int
    val_uint16: int
    val_int32: int
    val_uint32: int
    val_int64: int
    val_uint64: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., val_bool: bool = ..., val_byte: _Optional[int] = ..., val_char: _Optional[int] = ..., val_float32: _Optional[float] = ..., val_float64: _Optional[float] = ..., val_int8: _Optional[int] = ..., val_uint8: _Optional[int] = ..., val_int16: _Optional[int] = ..., val_uint16: _Optional[int] = ..., val_int32: _Optional[int] = ..., val_uint32: _Optional[int] = ..., val_int64: _Optional[int] = ..., val_uint64: _Optional[int] = ...) -> None: ...
