from make87_messages_ros2.rolling.rmf_scheduler_msgs.msg import payload_pb2 as _payload_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Trigger(_message.Message):
    __slots__ = ("name", "created_at", "at", "group", "payload")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    AT_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    name: str
    created_at: int
    at: int
    group: str
    payload: _payload_pb2.Payload
    def __init__(self, name: _Optional[str] = ..., created_at: _Optional[int] = ..., at: _Optional[int] = ..., group: _Optional[str] = ..., payload: _Optional[_Union[_payload_pb2.Payload, _Mapping]] = ...) -> None: ...
