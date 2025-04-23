from make87_messages_ros2.jazzy.rcss3d_agent_msgs.msg import spherical_pb2 as _spherical_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FieldLine(_message.Message):
    __slots__ = ("start", "end")
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    start: _spherical_pb2.Spherical
    end: _spherical_pb2.Spherical
    def __init__(self, start: _Optional[_Union[_spherical_pb2.Spherical, _Mapping]] = ..., end: _Optional[_Union[_spherical_pb2.Spherical, _Mapping]] = ...) -> None: ...
