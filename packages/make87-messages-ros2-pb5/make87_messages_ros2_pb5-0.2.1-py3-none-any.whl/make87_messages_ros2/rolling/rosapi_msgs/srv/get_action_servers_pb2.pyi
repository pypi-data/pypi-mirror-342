from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GetActionServersRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetActionServersResponse(_message.Message):
    __slots__ = ("action_servers",)
    ACTION_SERVERS_FIELD_NUMBER: _ClassVar[int]
    action_servers: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, action_servers: _Optional[_Iterable[str]] = ...) -> None: ...
