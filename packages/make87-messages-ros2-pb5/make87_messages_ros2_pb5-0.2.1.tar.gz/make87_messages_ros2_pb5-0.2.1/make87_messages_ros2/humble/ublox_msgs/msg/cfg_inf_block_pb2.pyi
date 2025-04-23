from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CfgINFBlock(_message.Message):
    __slots__ = ("header", "protocol_id", "reserved1", "inf_msg_mask")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_ID_FIELD_NUMBER: _ClassVar[int]
    RESERVED1_FIELD_NUMBER: _ClassVar[int]
    INF_MSG_MASK_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    protocol_id: int
    reserved1: _containers.RepeatedScalarFieldContainer[int]
    inf_msg_mask: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., protocol_id: _Optional[int] = ..., reserved1: _Optional[_Iterable[int]] = ..., inf_msg_mask: _Optional[_Iterable[int]] = ...) -> None: ...
