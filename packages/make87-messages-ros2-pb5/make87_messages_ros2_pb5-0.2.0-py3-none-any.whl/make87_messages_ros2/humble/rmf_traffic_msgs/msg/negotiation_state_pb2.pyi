from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rmf_traffic_msgs.msg import negotiation_forfeit_pb2 as _negotiation_forfeit_pb2
from make87_messages_ros2.humble.rmf_traffic_msgs.msg import negotiation_proposal_pb2 as _negotiation_proposal_pb2
from make87_messages_ros2.humble.rmf_traffic_msgs.msg import negotiation_rejection_pb2 as _negotiation_rejection_pb2
from make87_messages_ros2.humble.rmf_traffic_msgs.msg import negotiation_status_pb2 as _negotiation_status_pb2
from make87_messages_ros2.humble.rmf_traffic_msgs.msg import negotiation_tree_node_pb2 as _negotiation_tree_node_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NegotiationState(_message.Message):
    __slots__ = ("header", "status", "tree", "orphan_proposals", "orphan_rejections", "orphan_forfeits")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TREE_FIELD_NUMBER: _ClassVar[int]
    ORPHAN_PROPOSALS_FIELD_NUMBER: _ClassVar[int]
    ORPHAN_REJECTIONS_FIELD_NUMBER: _ClassVar[int]
    ORPHAN_FORFEITS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    status: _negotiation_status_pb2.NegotiationStatus
    tree: _containers.RepeatedCompositeFieldContainer[_negotiation_tree_node_pb2.NegotiationTreeNode]
    orphan_proposals: _containers.RepeatedCompositeFieldContainer[_negotiation_proposal_pb2.NegotiationProposal]
    orphan_rejections: _containers.RepeatedCompositeFieldContainer[_negotiation_rejection_pb2.NegotiationRejection]
    orphan_forfeits: _containers.RepeatedCompositeFieldContainer[_negotiation_forfeit_pb2.NegotiationForfeit]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., status: _Optional[_Union[_negotiation_status_pb2.NegotiationStatus, _Mapping]] = ..., tree: _Optional[_Iterable[_Union[_negotiation_tree_node_pb2.NegotiationTreeNode, _Mapping]]] = ..., orphan_proposals: _Optional[_Iterable[_Union[_negotiation_proposal_pb2.NegotiationProposal, _Mapping]]] = ..., orphan_rejections: _Optional[_Iterable[_Union[_negotiation_rejection_pb2.NegotiationRejection, _Mapping]]] = ..., orphan_forfeits: _Optional[_Iterable[_Union[_negotiation_forfeit_pb2.NegotiationForfeit, _Mapping]]] = ...) -> None: ...
