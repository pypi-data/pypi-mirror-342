from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class FieldSetWriteSrvRequest(_message.Message):
    __slots__ = ("field_set_selection_method_in", "active_field_set_in")
    FIELD_SET_SELECTION_METHOD_IN_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_SET_IN_FIELD_NUMBER: _ClassVar[int]
    field_set_selection_method_in: int
    active_field_set_in: int
    def __init__(self, field_set_selection_method_in: _Optional[int] = ..., active_field_set_in: _Optional[int] = ...) -> None: ...

class FieldSetWriteSrvResponse(_message.Message):
    __slots__ = ("field_set_selection_method", "active_field_set", "success")
    FIELD_SET_SELECTION_METHOD_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_SET_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    field_set_selection_method: int
    active_field_set: int
    success: bool
    def __init__(self, field_set_selection_method: _Optional[int] = ..., active_field_set: _Optional[int] = ..., success: bool = ...) -> None: ...
