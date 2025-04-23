from make87_messages_ros2.rolling.delphi_esr_msgs.msg import esr_track_motion_power_track_pb2 as _esr_track_motion_power_track_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EsrTrackMotionPowerGroup(_message.Message):
    __slots__ = ("header", "canmsg", "rolling_count_2", "can_id_group", "tracks")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CANMSG_FIELD_NUMBER: _ClassVar[int]
    ROLLING_COUNT_2_FIELD_NUMBER: _ClassVar[int]
    CAN_ID_GROUP_FIELD_NUMBER: _ClassVar[int]
    TRACKS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    canmsg: str
    rolling_count_2: int
    can_id_group: int
    tracks: _containers.RepeatedCompositeFieldContainer[_esr_track_motion_power_track_pb2.EsrTrackMotionPowerTrack]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., canmsg: _Optional[str] = ..., rolling_count_2: _Optional[int] = ..., can_id_group: _Optional[int] = ..., tracks: _Optional[_Iterable[_Union[_esr_track_motion_power_track_pb2.EsrTrackMotionPowerTrack, _Mapping]]] = ...) -> None: ...
