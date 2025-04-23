from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetPayloadRequest(_message.Message):
    __slots__ = ("header", "mass", "center_of_gravity")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MASS_FIELD_NUMBER: _ClassVar[int]
    CENTER_OF_GRAVITY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    mass: float
    center_of_gravity: _vector3_pb2.Vector3
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., mass: _Optional[float] = ..., center_of_gravity: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ...) -> None: ...

class SetPayloadResponse(_message.Message):
    __slots__ = ("header", "success")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ...) -> None: ...
