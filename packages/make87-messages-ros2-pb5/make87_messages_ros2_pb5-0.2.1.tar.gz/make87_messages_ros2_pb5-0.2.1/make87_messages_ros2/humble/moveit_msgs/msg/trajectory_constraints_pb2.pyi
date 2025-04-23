from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.moveit_msgs.msg import constraints_pb2 as _constraints_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TrajectoryConstraints(_message.Message):
    __slots__ = ("header", "constraints")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CONSTRAINTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    constraints: _containers.RepeatedCompositeFieldContainer[_constraints_pb2.Constraints]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., constraints: _Optional[_Iterable[_Union[_constraints_pb2.Constraints, _Mapping]]] = ...) -> None: ...
