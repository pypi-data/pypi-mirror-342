from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CfgINFBlock(_message.Message):
    __slots__ = ("protocol_id", "reserved1", "inf_msg_mask")
    PROTOCOL_ID_FIELD_NUMBER: _ClassVar[int]
    RESERVED1_FIELD_NUMBER: _ClassVar[int]
    INF_MSG_MASK_FIELD_NUMBER: _ClassVar[int]
    protocol_id: int
    reserved1: _containers.RepeatedScalarFieldContainer[int]
    inf_msg_mask: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, protocol_id: _Optional[int] = ..., reserved1: _Optional[_Iterable[int]] = ..., inf_msg_mask: _Optional[_Iterable[int]] = ...) -> None: ...
