from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Activation(_message.Message):
    __slots__ = ("operation_type", "activator", "activation")
    OPERATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACTIVATOR_FIELD_NUMBER: _ClassVar[int]
    ACTIVATION_FIELD_NUMBER: _ClassVar[int]
    operation_type: int
    activator: str
    activation: str
    def __init__(self, operation_type: _Optional[int] = ..., activator: _Optional[str] = ..., activation: _Optional[str] = ...) -> None: ...
