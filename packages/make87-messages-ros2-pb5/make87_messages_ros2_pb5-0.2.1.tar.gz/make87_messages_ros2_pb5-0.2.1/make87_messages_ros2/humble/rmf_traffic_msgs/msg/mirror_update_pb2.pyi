from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rmf_traffic_msgs.msg import schedule_identity_pb2 as _schedule_identity_pb2
from make87_messages_ros2.humble.rmf_traffic_msgs.msg import schedule_patch_pb2 as _schedule_patch_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MirrorUpdate(_message.Message):
    __slots__ = ("header", "node_id", "database_version", "patch", "is_remedial_update")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    DATABASE_VERSION_FIELD_NUMBER: _ClassVar[int]
    PATCH_FIELD_NUMBER: _ClassVar[int]
    IS_REMEDIAL_UPDATE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    node_id: _schedule_identity_pb2.ScheduleIdentity
    database_version: int
    patch: _schedule_patch_pb2.SchedulePatch
    is_remedial_update: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., node_id: _Optional[_Union[_schedule_identity_pb2.ScheduleIdentity, _Mapping]] = ..., database_version: _Optional[int] = ..., patch: _Optional[_Union[_schedule_patch_pb2.SchedulePatch, _Mapping]] = ..., is_remedial_update: bool = ...) -> None: ...
