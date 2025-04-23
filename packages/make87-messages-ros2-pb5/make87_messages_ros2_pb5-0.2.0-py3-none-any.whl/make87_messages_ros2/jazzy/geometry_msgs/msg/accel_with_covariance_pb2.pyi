from make87_messages_ros2.jazzy.geometry_msgs.msg import accel_pb2 as _accel_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AccelWithCovariance(_message.Message):
    __slots__ = ("accel", "covariance")
    ACCEL_FIELD_NUMBER: _ClassVar[int]
    COVARIANCE_FIELD_NUMBER: _ClassVar[int]
    accel: _accel_pb2.Accel
    covariance: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, accel: _Optional[_Union[_accel_pb2.Accel, _Mapping]] = ..., covariance: _Optional[_Iterable[float]] = ...) -> None: ...
