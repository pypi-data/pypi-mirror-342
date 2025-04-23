from make87_messages_ros2.jazzy.ublox_msgs.msg import rxm_rawsv_pb2 as _rxm_rawsv_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RxmRAW(_message.Message):
    __slots__ = ("rcv_tow", "week", "num_sv", "reserved1", "sv")
    RCV_TOW_FIELD_NUMBER: _ClassVar[int]
    WEEK_FIELD_NUMBER: _ClassVar[int]
    NUM_SV_FIELD_NUMBER: _ClassVar[int]
    RESERVED1_FIELD_NUMBER: _ClassVar[int]
    SV_FIELD_NUMBER: _ClassVar[int]
    rcv_tow: int
    week: int
    num_sv: int
    reserved1: int
    sv: _containers.RepeatedCompositeFieldContainer[_rxm_rawsv_pb2.RxmRAWSV]
    def __init__(self, rcv_tow: _Optional[int] = ..., week: _Optional[int] = ..., num_sv: _Optional[int] = ..., reserved1: _Optional[int] = ..., sv: _Optional[_Iterable[_Union[_rxm_rawsv_pb2.RxmRAWSV, _Mapping]]] = ...) -> None: ...
