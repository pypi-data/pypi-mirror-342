from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UdpSocketRequest(_message.Message):
    __slots__ = ("header", "local_address", "local_port", "remote_address", "remote_port", "is_broadcast")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LOCAL_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    LOCAL_PORT_FIELD_NUMBER: _ClassVar[int]
    REMOTE_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    REMOTE_PORT_FIELD_NUMBER: _ClassVar[int]
    IS_BROADCAST_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    local_address: str
    local_port: int
    remote_address: str
    remote_port: int
    is_broadcast: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., local_address: _Optional[str] = ..., local_port: _Optional[int] = ..., remote_address: _Optional[str] = ..., remote_port: _Optional[int] = ..., is_broadcast: bool = ...) -> None: ...

class UdpSocketResponse(_message.Message):
    __slots__ = ("header", "socket_created")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SOCKET_CREATED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    socket_created: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., socket_created: bool = ...) -> None: ...
