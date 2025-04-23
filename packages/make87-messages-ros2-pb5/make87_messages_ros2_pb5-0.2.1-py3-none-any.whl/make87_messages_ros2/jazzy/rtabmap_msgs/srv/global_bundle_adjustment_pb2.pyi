from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GlobalBundleAdjustmentRequest(_message.Message):
    __slots__ = ("type", "iterations", "pixel_variance", "voc_matches")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ITERATIONS_FIELD_NUMBER: _ClassVar[int]
    PIXEL_VARIANCE_FIELD_NUMBER: _ClassVar[int]
    VOC_MATCHES_FIELD_NUMBER: _ClassVar[int]
    type: int
    iterations: int
    pixel_variance: float
    voc_matches: bool
    def __init__(self, type: _Optional[int] = ..., iterations: _Optional[int] = ..., pixel_variance: _Optional[float] = ..., voc_matches: bool = ...) -> None: ...

class GlobalBundleAdjustmentResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
