from make87_messages_ros2.rolling.rmf_traffic_msgs.msg import itinerary_pb2 as _itinerary_pb2
from make87_messages_ros2.rolling.rmf_traffic_msgs.msg import negotiation_key_pb2 as _negotiation_key_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NegotiationRejection(_message.Message):
    __slots__ = ("conflict_version", "table", "rejected_by", "alternatives")
    CONFLICT_VERSION_FIELD_NUMBER: _ClassVar[int]
    TABLE_FIELD_NUMBER: _ClassVar[int]
    REJECTED_BY_FIELD_NUMBER: _ClassVar[int]
    ALTERNATIVES_FIELD_NUMBER: _ClassVar[int]
    conflict_version: int
    table: _containers.RepeatedCompositeFieldContainer[_negotiation_key_pb2.NegotiationKey]
    rejected_by: int
    alternatives: _containers.RepeatedCompositeFieldContainer[_itinerary_pb2.Itinerary]
    def __init__(self, conflict_version: _Optional[int] = ..., table: _Optional[_Iterable[_Union[_negotiation_key_pb2.NegotiationKey, _Mapping]]] = ..., rejected_by: _Optional[int] = ..., alternatives: _Optional[_Iterable[_Union[_itinerary_pb2.Itinerary, _Mapping]]] = ...) -> None: ...
