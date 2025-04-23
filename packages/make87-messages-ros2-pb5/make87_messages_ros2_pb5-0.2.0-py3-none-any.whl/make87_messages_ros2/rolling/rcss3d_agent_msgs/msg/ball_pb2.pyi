from make87_messages_ros2.rolling.rcss3d_agent_msgs.msg import spherical_pb2 as _spherical_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Ball(_message.Message):
    __slots__ = ("center",)
    CENTER_FIELD_NUMBER: _ClassVar[int]
    center: _spherical_pb2.Spherical
    def __init__(self, center: _Optional[_Union[_spherical_pb2.Spherical, _Mapping]] = ...) -> None: ...
