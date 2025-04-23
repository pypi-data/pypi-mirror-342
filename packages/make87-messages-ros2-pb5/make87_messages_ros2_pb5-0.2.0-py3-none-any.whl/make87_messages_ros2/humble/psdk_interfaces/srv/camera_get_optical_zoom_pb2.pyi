from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CameraGetOpticalZoomRequest(_message.Message):
    __slots__ = ("header", "payload_index")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_INDEX_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    payload_index: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., payload_index: _Optional[int] = ...) -> None: ...

class CameraGetOpticalZoomResponse(_message.Message):
    __slots__ = ("header", "success", "zoom_factor", "max_zoom_factor")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ZOOM_FACTOR_FIELD_NUMBER: _ClassVar[int]
    MAX_ZOOM_FACTOR_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    zoom_factor: float
    max_zoom_factor: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., zoom_factor: _Optional[float] = ..., max_zoom_factor: _Optional[float] = ...) -> None: ...
