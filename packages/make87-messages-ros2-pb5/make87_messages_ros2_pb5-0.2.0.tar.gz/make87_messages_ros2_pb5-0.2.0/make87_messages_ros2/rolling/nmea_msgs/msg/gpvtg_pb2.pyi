from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Gpvtg(_message.Message):
    __slots__ = ("header", "message_id", "track_t", "track_t_ref", "track_m", "track_m_ref", "speed_n", "speed_n_unit", "speed_k", "speed_k_unit", "mode_indicator")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    TRACK_T_FIELD_NUMBER: _ClassVar[int]
    TRACK_T_REF_FIELD_NUMBER: _ClassVar[int]
    TRACK_M_FIELD_NUMBER: _ClassVar[int]
    TRACK_M_REF_FIELD_NUMBER: _ClassVar[int]
    SPEED_N_FIELD_NUMBER: _ClassVar[int]
    SPEED_N_UNIT_FIELD_NUMBER: _ClassVar[int]
    SPEED_K_FIELD_NUMBER: _ClassVar[int]
    SPEED_K_UNIT_FIELD_NUMBER: _ClassVar[int]
    MODE_INDICATOR_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    message_id: str
    track_t: float
    track_t_ref: str
    track_m: float
    track_m_ref: str
    speed_n: float
    speed_n_unit: str
    speed_k: float
    speed_k_unit: str
    mode_indicator: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., message_id: _Optional[str] = ..., track_t: _Optional[float] = ..., track_t_ref: _Optional[str] = ..., track_m: _Optional[float] = ..., track_m_ref: _Optional[str] = ..., speed_n: _Optional[float] = ..., speed_n_unit: _Optional[str] = ..., speed_k: _Optional[float] = ..., speed_k_unit: _Optional[str] = ..., mode_indicator: _Optional[str] = ...) -> None: ...
