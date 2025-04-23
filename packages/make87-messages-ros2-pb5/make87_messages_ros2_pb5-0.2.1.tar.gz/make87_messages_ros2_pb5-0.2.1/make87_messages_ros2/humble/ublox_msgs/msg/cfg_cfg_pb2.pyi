from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CfgCFG(_message.Message):
    __slots__ = ("header", "clear_mask", "save_mask", "load_mask", "device_mask")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CLEAR_MASK_FIELD_NUMBER: _ClassVar[int]
    SAVE_MASK_FIELD_NUMBER: _ClassVar[int]
    LOAD_MASK_FIELD_NUMBER: _ClassVar[int]
    DEVICE_MASK_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    clear_mask: int
    save_mask: int
    load_mask: int
    device_mask: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., clear_mask: _Optional[int] = ..., save_mask: _Optional[int] = ..., load_mask: _Optional[int] = ..., device_mask: _Optional[int] = ...) -> None: ...
