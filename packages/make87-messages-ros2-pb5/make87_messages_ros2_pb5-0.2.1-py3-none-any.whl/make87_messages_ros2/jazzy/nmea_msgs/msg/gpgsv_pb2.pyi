from make87_messages_ros2.jazzy.nmea_msgs.msg import gpgsv_satellite_pb2 as _gpgsv_satellite_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Gpgsv(_message.Message):
    __slots__ = ("header", "message_id", "n_msgs", "msg_number", "n_satellites", "satellites")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    N_MSGS_FIELD_NUMBER: _ClassVar[int]
    MSG_NUMBER_FIELD_NUMBER: _ClassVar[int]
    N_SATELLITES_FIELD_NUMBER: _ClassVar[int]
    SATELLITES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    message_id: str
    n_msgs: int
    msg_number: int
    n_satellites: int
    satellites: _containers.RepeatedCompositeFieldContainer[_gpgsv_satellite_pb2.GpgsvSatellite]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., message_id: _Optional[str] = ..., n_msgs: _Optional[int] = ..., msg_number: _Optional[int] = ..., n_satellites: _Optional[int] = ..., satellites: _Optional[_Iterable[_Union[_gpgsv_satellite_pb2.GpgsvSatellite, _Mapping]]] = ...) -> None: ...
