from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rmf_traffic_msgs.msg import schedule_inconsistency_range_pb2 as _schedule_inconsistency_range_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ScheduleInconsistency(_message.Message):
    __slots__ = ("header", "participant", "ranges", "last_known_itinerary", "last_known_progress")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PARTICIPANT_FIELD_NUMBER: _ClassVar[int]
    RANGES_FIELD_NUMBER: _ClassVar[int]
    LAST_KNOWN_ITINERARY_FIELD_NUMBER: _ClassVar[int]
    LAST_KNOWN_PROGRESS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    participant: int
    ranges: _containers.RepeatedCompositeFieldContainer[_schedule_inconsistency_range_pb2.ScheduleInconsistencyRange]
    last_known_itinerary: int
    last_known_progress: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., participant: _Optional[int] = ..., ranges: _Optional[_Iterable[_Union[_schedule_inconsistency_range_pb2.ScheduleInconsistencyRange, _Mapping]]] = ..., last_known_itinerary: _Optional[int] = ..., last_known_progress: _Optional[int] = ...) -> None: ...
