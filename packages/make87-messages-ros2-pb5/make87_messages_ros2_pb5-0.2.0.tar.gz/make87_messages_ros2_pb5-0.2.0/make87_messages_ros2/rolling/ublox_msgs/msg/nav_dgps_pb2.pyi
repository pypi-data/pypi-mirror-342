from make87_messages_ros2.rolling.ublox_msgs.msg import nav_dgpssv_pb2 as _nav_dgpssv_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NavDGPS(_message.Message):
    __slots__ = ("i_tow", "age", "base_id", "base_health", "num_ch", "status", "reserved1", "sv")
    I_TOW_FIELD_NUMBER: _ClassVar[int]
    AGE_FIELD_NUMBER: _ClassVar[int]
    BASE_ID_FIELD_NUMBER: _ClassVar[int]
    BASE_HEALTH_FIELD_NUMBER: _ClassVar[int]
    NUM_CH_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    RESERVED1_FIELD_NUMBER: _ClassVar[int]
    SV_FIELD_NUMBER: _ClassVar[int]
    i_tow: int
    age: int
    base_id: int
    base_health: int
    num_ch: int
    status: int
    reserved1: int
    sv: _containers.RepeatedCompositeFieldContainer[_nav_dgpssv_pb2.NavDGPSSV]
    def __init__(self, i_tow: _Optional[int] = ..., age: _Optional[int] = ..., base_id: _Optional[int] = ..., base_health: _Optional[int] = ..., num_ch: _Optional[int] = ..., status: _Optional[int] = ..., reserved1: _Optional[int] = ..., sv: _Optional[_Iterable[_Union[_nav_dgpssv_pb2.NavDGPSSV, _Mapping]]] = ...) -> None: ...
