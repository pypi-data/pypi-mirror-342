from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SbgStatusAiding(_message.Message):
    __slots__ = ("gps1_pos_recv", "gps1_vel_recv", "gps1_hdt_recv", "gps1_utc_recv", "gps2_pos_recv", "gps2_vel_recv", "gps2_hdt_recv", "gps2_utc_recv", "mag_recv", "odo_recv", "dvl_recv", "usbl_recv", "depth_recv", "air_data_recv", "user_pos_recv", "user_vel_recv", "user_heading_recv")
    GPS1_POS_RECV_FIELD_NUMBER: _ClassVar[int]
    GPS1_VEL_RECV_FIELD_NUMBER: _ClassVar[int]
    GPS1_HDT_RECV_FIELD_NUMBER: _ClassVar[int]
    GPS1_UTC_RECV_FIELD_NUMBER: _ClassVar[int]
    GPS2_POS_RECV_FIELD_NUMBER: _ClassVar[int]
    GPS2_VEL_RECV_FIELD_NUMBER: _ClassVar[int]
    GPS2_HDT_RECV_FIELD_NUMBER: _ClassVar[int]
    GPS2_UTC_RECV_FIELD_NUMBER: _ClassVar[int]
    MAG_RECV_FIELD_NUMBER: _ClassVar[int]
    ODO_RECV_FIELD_NUMBER: _ClassVar[int]
    DVL_RECV_FIELD_NUMBER: _ClassVar[int]
    USBL_RECV_FIELD_NUMBER: _ClassVar[int]
    DEPTH_RECV_FIELD_NUMBER: _ClassVar[int]
    AIR_DATA_RECV_FIELD_NUMBER: _ClassVar[int]
    USER_POS_RECV_FIELD_NUMBER: _ClassVar[int]
    USER_VEL_RECV_FIELD_NUMBER: _ClassVar[int]
    USER_HEADING_RECV_FIELD_NUMBER: _ClassVar[int]
    gps1_pos_recv: bool
    gps1_vel_recv: bool
    gps1_hdt_recv: bool
    gps1_utc_recv: bool
    gps2_pos_recv: bool
    gps2_vel_recv: bool
    gps2_hdt_recv: bool
    gps2_utc_recv: bool
    mag_recv: bool
    odo_recv: bool
    dvl_recv: bool
    usbl_recv: bool
    depth_recv: bool
    air_data_recv: bool
    user_pos_recv: bool
    user_vel_recv: bool
    user_heading_recv: bool
    def __init__(self, gps1_pos_recv: bool = ..., gps1_vel_recv: bool = ..., gps1_hdt_recv: bool = ..., gps1_utc_recv: bool = ..., gps2_pos_recv: bool = ..., gps2_vel_recv: bool = ..., gps2_hdt_recv: bool = ..., gps2_utc_recv: bool = ..., mag_recv: bool = ..., odo_recv: bool = ..., dvl_recv: bool = ..., usbl_recv: bool = ..., depth_recv: bool = ..., air_data_recv: bool = ..., user_pos_recv: bool = ..., user_vel_recv: bool = ..., user_heading_recv: bool = ...) -> None: ...
