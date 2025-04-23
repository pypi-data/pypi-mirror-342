from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class IntegerRange(_message.Message):
    __slots__ = ("from_value", "to_value", "step")
    FROM_VALUE_FIELD_NUMBER: _ClassVar[int]
    TO_VALUE_FIELD_NUMBER: _ClassVar[int]
    STEP_FIELD_NUMBER: _ClassVar[int]
    from_value: int
    to_value: int
    step: int
    def __init__(self, from_value: _Optional[int] = ..., to_value: _Optional[int] = ..., step: _Optional[int] = ...) -> None: ...
