from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rmf_traffic_msgs.msg import schedule_identity_pb2 as _schedule_identity_pb2
from make87_messages_ros2.humble.rmf_traffic_msgs.msg import schedule_query_pb2 as _schedule_query_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ScheduleQueries(_message.Message):
    __slots__ = ("header", "node_id", "queries", "query_ids")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    QUERIES_FIELD_NUMBER: _ClassVar[int]
    QUERY_IDS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    node_id: _schedule_identity_pb2.ScheduleIdentity
    queries: _containers.RepeatedCompositeFieldContainer[_schedule_query_pb2.ScheduleQuery]
    query_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., node_id: _Optional[_Union[_schedule_identity_pb2.ScheduleIdentity, _Mapping]] = ..., queries: _Optional[_Iterable[_Union[_schedule_query_pb2.ScheduleQuery, _Mapping]]] = ..., query_ids: _Optional[_Iterable[int]] = ...) -> None: ...
