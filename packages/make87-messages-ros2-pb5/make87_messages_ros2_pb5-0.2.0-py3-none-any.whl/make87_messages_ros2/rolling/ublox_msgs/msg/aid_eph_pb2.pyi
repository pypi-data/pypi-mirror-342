from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AidEPH(_message.Message):
    __slots__ = ("svid", "how", "sf1d", "sf2d", "sf3d")
    SVID_FIELD_NUMBER: _ClassVar[int]
    HOW_FIELD_NUMBER: _ClassVar[int]
    SF1D_FIELD_NUMBER: _ClassVar[int]
    SF2D_FIELD_NUMBER: _ClassVar[int]
    SF3D_FIELD_NUMBER: _ClassVar[int]
    svid: int
    how: int
    sf1d: _containers.RepeatedScalarFieldContainer[int]
    sf2d: _containers.RepeatedScalarFieldContainer[int]
    sf3d: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, svid: _Optional[int] = ..., how: _Optional[int] = ..., sf1d: _Optional[_Iterable[int]] = ..., sf2d: _Optional[_Iterable[int]] = ..., sf3d: _Optional[_Iterable[int]] = ...) -> None: ...
