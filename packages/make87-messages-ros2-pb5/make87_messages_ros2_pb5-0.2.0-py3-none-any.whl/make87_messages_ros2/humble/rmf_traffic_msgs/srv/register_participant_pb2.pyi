from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rmf_traffic_msgs.msg import participant_description_pb2 as _participant_description_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RegisterParticipantRequest(_message.Message):
    __slots__ = ("header", "description")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    description: _participant_description_pb2.ParticipantDescription
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., description: _Optional[_Union[_participant_description_pb2.ParticipantDescription, _Mapping]] = ...) -> None: ...

class RegisterParticipantResponse(_message.Message):
    __slots__ = ("header", "participant_id", "last_itinerary_version", "last_plan_id", "next_storage_base", "error")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PARTICIPANT_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_ITINERARY_VERSION_FIELD_NUMBER: _ClassVar[int]
    LAST_PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    NEXT_STORAGE_BASE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    participant_id: int
    last_itinerary_version: int
    last_plan_id: int
    next_storage_base: int
    error: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., participant_id: _Optional[int] = ..., last_itinerary_version: _Optional[int] = ..., last_plan_id: _Optional[int] = ..., next_storage_base: _Optional[int] = ..., error: _Optional[str] = ...) -> None: ...
