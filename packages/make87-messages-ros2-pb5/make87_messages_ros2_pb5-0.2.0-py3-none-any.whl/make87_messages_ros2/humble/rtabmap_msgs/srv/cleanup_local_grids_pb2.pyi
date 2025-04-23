from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CleanupLocalGridsRequest(_message.Message):
    __slots__ = ("header", "radius", "filter_scans")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    RADIUS_FIELD_NUMBER: _ClassVar[int]
    FILTER_SCANS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    radius: int
    filter_scans: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., radius: _Optional[int] = ..., filter_scans: bool = ...) -> None: ...

class CleanupLocalGridsResponse(_message.Message):
    __slots__ = ("header", "modified")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MODIFIED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    modified: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., modified: _Optional[int] = ...) -> None: ...
