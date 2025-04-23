from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ClientExpandMapEnableRequest(_message.Message):
    __slots__ = ("header", "prior_map_name")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PRIOR_MAP_NAME_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    prior_map_name: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., prior_map_name: _Optional[str] = ...) -> None: ...

class ClientExpandMapEnableResponse(_message.Message):
    __slots__ = ("header",)
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...
