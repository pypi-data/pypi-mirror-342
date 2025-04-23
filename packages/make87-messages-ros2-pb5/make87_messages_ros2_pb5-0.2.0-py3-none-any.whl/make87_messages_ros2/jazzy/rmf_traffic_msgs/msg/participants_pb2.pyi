from make87_messages_ros2.jazzy.rmf_traffic_msgs.msg import participant_pb2 as _participant_pb2
from make87_messages_ros2.jazzy.rmf_traffic_msgs.msg import schedule_identity_pb2 as _schedule_identity_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Participants(_message.Message):
    __slots__ = ("node_id", "participants")
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    PARTICIPANTS_FIELD_NUMBER: _ClassVar[int]
    node_id: _schedule_identity_pb2.ScheduleIdentity
    participants: _containers.RepeatedCompositeFieldContainer[_participant_pb2.Participant]
    def __init__(self, node_id: _Optional[_Union[_schedule_identity_pb2.ScheduleIdentity, _Mapping]] = ..., participants: _Optional[_Iterable[_Union[_participant_pb2.Participant, _Mapping]]] = ...) -> None: ...
