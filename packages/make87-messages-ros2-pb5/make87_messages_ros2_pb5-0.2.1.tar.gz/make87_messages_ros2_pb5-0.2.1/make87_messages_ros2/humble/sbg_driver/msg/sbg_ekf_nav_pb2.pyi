from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from make87_messages_ros2.humble.sbg_driver.msg import sbg_ekf_status_pb2 as _sbg_ekf_status_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SbgEkfNav(_message.Message):
    __slots__ = ("header", "ros2_header", "time_stamp", "velocity", "velocity_accuracy", "latitude", "longitude", "altitude", "undulation", "position_accuracy", "status")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    TIME_STAMP_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_ACCURACY_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_FIELD_NUMBER: _ClassVar[int]
    UNDULATION_FIELD_NUMBER: _ClassVar[int]
    POSITION_ACCURACY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    time_stamp: int
    velocity: _vector3_pb2.Vector3
    velocity_accuracy: _vector3_pb2.Vector3
    latitude: float
    longitude: float
    altitude: float
    undulation: float
    position_accuracy: _vector3_pb2.Vector3
    status: _sbg_ekf_status_pb2.SbgEkfStatus
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., time_stamp: _Optional[int] = ..., velocity: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., velocity_accuracy: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., latitude: _Optional[float] = ..., longitude: _Optional[float] = ..., altitude: _Optional[float] = ..., undulation: _Optional[float] = ..., position_accuracy: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., status: _Optional[_Union[_sbg_ekf_status_pb2.SbgEkfStatus, _Mapping]] = ...) -> None: ...
