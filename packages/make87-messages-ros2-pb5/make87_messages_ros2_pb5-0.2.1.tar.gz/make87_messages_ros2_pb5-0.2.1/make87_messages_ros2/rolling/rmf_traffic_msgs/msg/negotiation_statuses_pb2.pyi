from make87_messages_ros2.rolling.rmf_traffic_msgs.msg import negotiation_status_pb2 as _negotiation_status_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NegotiationStatuses(_message.Message):
    __slots__ = ("negotiations",)
    NEGOTIATIONS_FIELD_NUMBER: _ClassVar[int]
    negotiations: _containers.RepeatedCompositeFieldContainer[_negotiation_status_pb2.NegotiationStatus]
    def __init__(self, negotiations: _Optional[_Iterable[_Union[_negotiation_status_pb2.NegotiationStatus, _Mapping]]] = ...) -> None: ...
