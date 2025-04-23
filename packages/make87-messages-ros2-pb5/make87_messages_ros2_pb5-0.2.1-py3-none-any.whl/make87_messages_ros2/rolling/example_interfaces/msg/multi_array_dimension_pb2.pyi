from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class MultiArrayDimension(_message.Message):
    __slots__ = ("label", "size", "stride")
    LABEL_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    STRIDE_FIELD_NUMBER: _ClassVar[int]
    label: str
    size: int
    stride: int
    def __init__(self, label: _Optional[str] = ..., size: _Optional[int] = ..., stride: _Optional[int] = ...) -> None: ...
