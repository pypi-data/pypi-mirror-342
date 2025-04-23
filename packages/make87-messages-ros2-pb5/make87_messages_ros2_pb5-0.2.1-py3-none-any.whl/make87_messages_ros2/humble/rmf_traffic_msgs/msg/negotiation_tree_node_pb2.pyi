from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rmf_traffic_msgs.msg import negotiation_key_pb2 as _negotiation_key_pb2
from make87_messages_ros2.humble.rmf_traffic_msgs.msg import route_pb2 as _route_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NegotiationTreeNode(_message.Message):
    __slots__ = ("header", "parent", "key", "rejected", "itinerary")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PARENT_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    REJECTED_FIELD_NUMBER: _ClassVar[int]
    ITINERARY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    parent: int
    key: _negotiation_key_pb2.NegotiationKey
    rejected: bool
    itinerary: _containers.RepeatedCompositeFieldContainer[_route_pb2.Route]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., parent: _Optional[int] = ..., key: _Optional[_Union[_negotiation_key_pb2.NegotiationKey, _Mapping]] = ..., rejected: bool = ..., itinerary: _Optional[_Iterable[_Union[_route_pb2.Route, _Mapping]]] = ...) -> None: ...
