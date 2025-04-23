from make87_messages_ros2.jazzy.ublox_msgs.msg import nav_svinfosv_pb2 as _nav_svinfosv_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NavSVINFO(_message.Message):
    __slots__ = ("i_tow", "num_ch", "global_flags", "reserved2", "sv")
    I_TOW_FIELD_NUMBER: _ClassVar[int]
    NUM_CH_FIELD_NUMBER: _ClassVar[int]
    GLOBAL_FLAGS_FIELD_NUMBER: _ClassVar[int]
    RESERVED2_FIELD_NUMBER: _ClassVar[int]
    SV_FIELD_NUMBER: _ClassVar[int]
    i_tow: int
    num_ch: int
    global_flags: int
    reserved2: int
    sv: _containers.RepeatedCompositeFieldContainer[_nav_svinfosv_pb2.NavSVINFOSV]
    def __init__(self, i_tow: _Optional[int] = ..., num_ch: _Optional[int] = ..., global_flags: _Optional[int] = ..., reserved2: _Optional[int] = ..., sv: _Optional[_Iterable[_Union[_nav_svinfosv_pb2.NavSVINFOSV, _Mapping]]] = ...) -> None: ...
