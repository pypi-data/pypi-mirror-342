from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RegionOfInterest(_message.Message):
    __slots__ = ("x_offset", "y_offset", "height", "width", "do_rectify")
    X_OFFSET_FIELD_NUMBER: _ClassVar[int]
    Y_OFFSET_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    DO_RECTIFY_FIELD_NUMBER: _ClassVar[int]
    x_offset: int
    y_offset: int
    height: int
    width: int
    do_rectify: bool
    def __init__(self, x_offset: _Optional[int] = ..., y_offset: _Optional[int] = ..., height: _Optional[int] = ..., width: _Optional[int] = ..., do_rectify: bool = ...) -> None: ...
