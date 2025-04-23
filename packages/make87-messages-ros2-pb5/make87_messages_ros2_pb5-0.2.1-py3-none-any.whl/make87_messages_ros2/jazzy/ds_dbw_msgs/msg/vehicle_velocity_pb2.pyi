from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VehicleVelocity(_message.Message):
    __slots__ = ("header", "vehicle_velocity_brake", "vehicle_velocity_propulsion", "dir_src")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    VEHICLE_VELOCITY_BRAKE_FIELD_NUMBER: _ClassVar[int]
    VEHICLE_VELOCITY_PROPULSION_FIELD_NUMBER: _ClassVar[int]
    DIR_SRC_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    vehicle_velocity_brake: float
    vehicle_velocity_propulsion: float
    dir_src: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., vehicle_velocity_brake: _Optional[float] = ..., vehicle_velocity_propulsion: _Optional[float] = ..., dir_src: _Optional[int] = ...) -> None: ...
