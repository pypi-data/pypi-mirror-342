from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rcss3d_agent_msgs.msg import spherical_pb2 as _spherical_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FieldLine(_message.Message):
    __slots__ = ("header", "start", "end")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    start: _spherical_pb2.Spherical
    end: _spherical_pb2.Spherical
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., start: _Optional[_Union[_spherical_pb2.Spherical, _Mapping]] = ..., end: _Optional[_Union[_spherical_pb2.Spherical, _Mapping]] = ...) -> None: ...
