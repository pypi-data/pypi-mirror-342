from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class UdpSocketRequest(_message.Message):
    __slots__ = ("local_address", "local_port", "remote_address", "remote_port", "is_broadcast")
    LOCAL_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    LOCAL_PORT_FIELD_NUMBER: _ClassVar[int]
    REMOTE_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    REMOTE_PORT_FIELD_NUMBER: _ClassVar[int]
    IS_BROADCAST_FIELD_NUMBER: _ClassVar[int]
    local_address: str
    local_port: int
    remote_address: str
    remote_port: int
    is_broadcast: bool
    def __init__(self, local_address: _Optional[str] = ..., local_port: _Optional[int] = ..., remote_address: _Optional[str] = ..., remote_port: _Optional[int] = ..., is_broadcast: bool = ...) -> None: ...

class UdpSocketResponse(_message.Message):
    __slots__ = ("socket_created",)
    SOCKET_CREATED_FIELD_NUMBER: _ClassVar[int]
    socket_created: bool
    def __init__(self, socket_created: bool = ...) -> None: ...
