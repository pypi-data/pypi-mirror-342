from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class COReadIDRequest(_message.Message):
    __slots__ = ("header", "nodeid", "index", "subindex", "canopen_datatype")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NODEID_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    SUBINDEX_FIELD_NUMBER: _ClassVar[int]
    CANOPEN_DATATYPE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    nodeid: int
    index: int
    subindex: int
    canopen_datatype: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., nodeid: _Optional[int] = ..., index: _Optional[int] = ..., subindex: _Optional[int] = ..., canopen_datatype: _Optional[int] = ...) -> None: ...

class COReadIDResponse(_message.Message):
    __slots__ = ("header", "success", "data")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    data: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., data: _Optional[int] = ...) -> None: ...
