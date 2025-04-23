from make87_messages_ros2.rolling.geographic_msgs.msg import geographic_map_changes_pb2 as _geographic_map_changes_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UpdateGeographicMapRequest(_message.Message):
    __slots__ = ("updates",)
    UPDATES_FIELD_NUMBER: _ClassVar[int]
    updates: _geographic_map_changes_pb2.GeographicMapChanges
    def __init__(self, updates: _Optional[_Union[_geographic_map_changes_pb2.GeographicMapChanges, _Mapping]] = ...) -> None: ...

class UpdateGeographicMapResponse(_message.Message):
    __slots__ = ("success", "status")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    status: str
    def __init__(self, success: bool = ..., status: _Optional[str] = ...) -> None: ...
