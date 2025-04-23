from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.tuw_object_msgs.msg import object_pb2 as _object_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ObjectWithCovariance(_message.Message):
    __slots__ = ("header", "object", "covariance_pose", "covariance_twist", "correlation")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    COVARIANCE_POSE_FIELD_NUMBER: _ClassVar[int]
    COVARIANCE_TWIST_FIELD_NUMBER: _ClassVar[int]
    CORRELATION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    object: _object_pb2.Object
    covariance_pose: _containers.RepeatedScalarFieldContainer[float]
    covariance_twist: _containers.RepeatedScalarFieldContainer[float]
    correlation: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., object: _Optional[_Union[_object_pb2.Object, _Mapping]] = ..., covariance_pose: _Optional[_Iterable[float]] = ..., covariance_twist: _Optional[_Iterable[float]] = ..., correlation: _Optional[_Iterable[float]] = ...) -> None: ...
