from make87_messages_ros2.rolling.rmf_traffic_msgs.msg import negotiation_key_pb2 as _negotiation_key_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NegotiationConclusion(_message.Message):
    __slots__ = ("conflict_version", "resolved", "table")
    CONFLICT_VERSION_FIELD_NUMBER: _ClassVar[int]
    RESOLVED_FIELD_NUMBER: _ClassVar[int]
    TABLE_FIELD_NUMBER: _ClassVar[int]
    conflict_version: int
    resolved: bool
    table: _containers.RepeatedCompositeFieldContainer[_negotiation_key_pb2.NegotiationKey]
    def __init__(self, conflict_version: _Optional[int] = ..., resolved: bool = ..., table: _Optional[_Iterable[_Union[_negotiation_key_pb2.NegotiationKey, _Mapping]]] = ...) -> None: ...
