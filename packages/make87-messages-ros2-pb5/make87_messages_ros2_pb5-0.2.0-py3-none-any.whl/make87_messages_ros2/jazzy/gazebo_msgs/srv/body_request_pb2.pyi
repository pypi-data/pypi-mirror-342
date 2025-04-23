from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class BodyRequestRequest(_message.Message):
    __slots__ = ("body_name",)
    BODY_NAME_FIELD_NUMBER: _ClassVar[int]
    body_name: str
    def __init__(self, body_name: _Optional[str] = ...) -> None: ...

class BodyRequestResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
