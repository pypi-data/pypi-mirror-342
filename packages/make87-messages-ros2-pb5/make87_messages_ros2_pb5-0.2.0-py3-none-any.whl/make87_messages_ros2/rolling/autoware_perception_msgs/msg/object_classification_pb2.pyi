from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ObjectClassification(_message.Message):
    __slots__ = ("label", "probability")
    LABEL_FIELD_NUMBER: _ClassVar[int]
    PROBABILITY_FIELD_NUMBER: _ClassVar[int]
    label: int
    probability: float
    def __init__(self, label: _Optional[int] = ..., probability: _Optional[float] = ...) -> None: ...
