from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from make87_messages_ros2.humble.sbg_driver.msg import sbg_gps_pos_status_pb2 as _sbg_gps_pos_status_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SbgGpsPos(_message.Message):
    __slots__ = ("header", "ros2_header", "time_stamp", "status", "gps_tow", "latitude", "longitude", "altitude", "undulation", "position_accuracy", "num_sv_tracked", "num_sv_used", "base_station_id", "diff_age")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    TIME_STAMP_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    GPS_TOW_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_FIELD_NUMBER: _ClassVar[int]
    UNDULATION_FIELD_NUMBER: _ClassVar[int]
    POSITION_ACCURACY_FIELD_NUMBER: _ClassVar[int]
    NUM_SV_TRACKED_FIELD_NUMBER: _ClassVar[int]
    NUM_SV_USED_FIELD_NUMBER: _ClassVar[int]
    BASE_STATION_ID_FIELD_NUMBER: _ClassVar[int]
    DIFF_AGE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    time_stamp: int
    status: _sbg_gps_pos_status_pb2.SbgGpsPosStatus
    gps_tow: int
    latitude: float
    longitude: float
    altitude: float
    undulation: float
    position_accuracy: _vector3_pb2.Vector3
    num_sv_tracked: int
    num_sv_used: int
    base_station_id: int
    diff_age: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., time_stamp: _Optional[int] = ..., status: _Optional[_Union[_sbg_gps_pos_status_pb2.SbgGpsPosStatus, _Mapping]] = ..., gps_tow: _Optional[int] = ..., latitude: _Optional[float] = ..., longitude: _Optional[float] = ..., altitude: _Optional[float] = ..., undulation: _Optional[float] = ..., position_accuracy: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., num_sv_tracked: _Optional[int] = ..., num_sv_used: _Optional[int] = ..., base_station_id: _Optional[int] = ..., diff_age: _Optional[int] = ...) -> None: ...
