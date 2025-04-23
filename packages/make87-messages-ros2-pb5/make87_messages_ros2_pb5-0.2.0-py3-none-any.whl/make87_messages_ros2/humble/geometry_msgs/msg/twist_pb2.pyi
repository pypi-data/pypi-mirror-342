from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Twist(_message.Message):
    __slots__ = ("header", "linear", "angular")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LINEAR_FIELD_NUMBER: _ClassVar[int]
    ANGULAR_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    linear: _vector3_pb2.Vector3
    angular: _vector3_pb2.Vector3
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., linear: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., angular: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ...) -> None: ...
