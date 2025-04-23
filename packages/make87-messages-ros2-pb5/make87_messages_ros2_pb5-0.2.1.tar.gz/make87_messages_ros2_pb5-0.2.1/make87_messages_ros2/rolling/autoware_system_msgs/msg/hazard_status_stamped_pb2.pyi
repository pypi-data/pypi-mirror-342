from make87_messages_ros2.rolling.autoware_system_msgs.msg import hazard_status_pb2 as _hazard_status_pb2
from make87_messages_ros2.rolling.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HazardStatusStamped(_message.Message):
    __slots__ = ("stamp", "status")
    STAMP_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    stamp: _time_pb2.Time
    status: _hazard_status_pb2.HazardStatus
    def __init__(self, stamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., status: _Optional[_Union[_hazard_status_pb2.HazardStatus, _Mapping]] = ...) -> None: ...
