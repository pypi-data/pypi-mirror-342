from make87_messages_ros2.jazzy.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from make87_messages_ros2.jazzy.sbg_driver.msg import sbg_mag_status_pb2 as _sbg_mag_status_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SbgMag(_message.Message):
    __slots__ = ("header", "time_stamp", "mag", "accel", "status")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TIME_STAMP_FIELD_NUMBER: _ClassVar[int]
    MAG_FIELD_NUMBER: _ClassVar[int]
    ACCEL_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    time_stamp: int
    mag: _vector3_pb2.Vector3
    accel: _vector3_pb2.Vector3
    status: _sbg_mag_status_pb2.SbgMagStatus
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., time_stamp: _Optional[int] = ..., mag: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., accel: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., status: _Optional[_Union[_sbg_mag_status_pb2.SbgMagStatus, _Mapping]] = ...) -> None: ...
