from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rmf_traffic_msgs.msg import schedule_change_cull_pb2 as _schedule_change_cull_pb2
from make87_messages_ros2.humble.rmf_traffic_msgs.msg import schedule_participant_patch_pb2 as _schedule_participant_patch_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SchedulePatch(_message.Message):
    __slots__ = ("header", "participants", "cull", "has_base_version", "base_version", "latest_version")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PARTICIPANTS_FIELD_NUMBER: _ClassVar[int]
    CULL_FIELD_NUMBER: _ClassVar[int]
    HAS_BASE_VERSION_FIELD_NUMBER: _ClassVar[int]
    BASE_VERSION_FIELD_NUMBER: _ClassVar[int]
    LATEST_VERSION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    participants: _containers.RepeatedCompositeFieldContainer[_schedule_participant_patch_pb2.ScheduleParticipantPatch]
    cull: _containers.RepeatedCompositeFieldContainer[_schedule_change_cull_pb2.ScheduleChangeCull]
    has_base_version: bool
    base_version: int
    latest_version: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., participants: _Optional[_Iterable[_Union[_schedule_participant_patch_pb2.ScheduleParticipantPatch, _Mapping]]] = ..., cull: _Optional[_Iterable[_Union[_schedule_change_cull_pb2.ScheduleChangeCull, _Mapping]]] = ..., has_base_version: bool = ..., base_version: _Optional[int] = ..., latest_version: _Optional[int] = ...) -> None: ...
