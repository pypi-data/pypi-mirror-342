from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Ack(_message.Message):
    __slots__ = ("cls_id", "msg_id")
    CLS_ID_FIELD_NUMBER: _ClassVar[int]
    MSG_ID_FIELD_NUMBER: _ClassVar[int]
    cls_id: int
    msg_id: int
    def __init__(self, cls_id: _Optional[int] = ..., msg_id: _Optional[int] = ...) -> None: ...
