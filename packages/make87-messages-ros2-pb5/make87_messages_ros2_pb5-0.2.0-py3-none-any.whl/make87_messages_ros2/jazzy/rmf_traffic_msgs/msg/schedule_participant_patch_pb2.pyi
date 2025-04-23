from make87_messages_ros2.jazzy.rmf_traffic_msgs.msg import schedule_change_add_pb2 as _schedule_change_add_pb2
from make87_messages_ros2.jazzy.rmf_traffic_msgs.msg import schedule_change_delay_pb2 as _schedule_change_delay_pb2
from make87_messages_ros2.jazzy.rmf_traffic_msgs.msg import schedule_change_progress_pb2 as _schedule_change_progress_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ScheduleParticipantPatch(_message.Message):
    __slots__ = ("participant_id", "itinerary_version", "erasures", "delays", "additions", "progress")
    PARTICIPANT_ID_FIELD_NUMBER: _ClassVar[int]
    ITINERARY_VERSION_FIELD_NUMBER: _ClassVar[int]
    ERASURES_FIELD_NUMBER: _ClassVar[int]
    DELAYS_FIELD_NUMBER: _ClassVar[int]
    ADDITIONS_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    participant_id: int
    itinerary_version: int
    erasures: _containers.RepeatedScalarFieldContainer[int]
    delays: _containers.RepeatedCompositeFieldContainer[_schedule_change_delay_pb2.ScheduleChangeDelay]
    additions: _schedule_change_add_pb2.ScheduleChangeAdd
    progress: _schedule_change_progress_pb2.ScheduleChangeProgress
    def __init__(self, participant_id: _Optional[int] = ..., itinerary_version: _Optional[int] = ..., erasures: _Optional[_Iterable[int]] = ..., delays: _Optional[_Iterable[_Union[_schedule_change_delay_pb2.ScheduleChangeDelay, _Mapping]]] = ..., additions: _Optional[_Union[_schedule_change_add_pb2.ScheduleChangeAdd, _Mapping]] = ..., progress: _Optional[_Union[_schedule_change_progress_pb2.ScheduleChangeProgress, _Mapping]] = ...) -> None: ...
