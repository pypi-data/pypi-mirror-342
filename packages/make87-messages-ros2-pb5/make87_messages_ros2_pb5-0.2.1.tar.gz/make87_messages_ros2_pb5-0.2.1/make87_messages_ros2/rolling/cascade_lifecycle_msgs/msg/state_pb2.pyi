from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class State(_message.Message):
    __slots__ = ("state", "node_name")
    STATE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    state: int
    node_name: str
    def __init__(self, state: _Optional[int] = ..., node_name: _Optional[str] = ...) -> None: ...
