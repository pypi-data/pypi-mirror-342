from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import accel_pb2 as _accel_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import twist_with_covariance_pb2 as _twist_with_covariance_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EgoVehicleData(_message.Message):
    __slots__ = ("header", "velocity", "acceleration")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_FIELD_NUMBER: _ClassVar[int]
    ACCELERATION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    velocity: _twist_with_covariance_pb2.TwistWithCovariance
    acceleration: _accel_pb2.Accel
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., velocity: _Optional[_Union[_twist_with_covariance_pb2.TwistWithCovariance, _Mapping]] = ..., acceleration: _Optional[_Union[_accel_pb2.Accel, _Mapping]] = ...) -> None: ...
