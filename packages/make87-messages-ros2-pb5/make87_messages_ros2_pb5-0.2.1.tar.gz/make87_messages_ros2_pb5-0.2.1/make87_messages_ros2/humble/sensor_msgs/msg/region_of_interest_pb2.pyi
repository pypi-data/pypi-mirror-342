from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RegionOfInterest(_message.Message):
    __slots__ = ("header", "x_offset", "y_offset", "height", "width", "do_rectify")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    X_OFFSET_FIELD_NUMBER: _ClassVar[int]
    Y_OFFSET_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    DO_RECTIFY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    x_offset: int
    y_offset: int
    height: int
    width: int
    do_rectify: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., x_offset: _Optional[int] = ..., y_offset: _Optional[int] = ..., height: _Optional[int] = ..., width: _Optional[int] = ..., do_rectify: bool = ...) -> None: ...
