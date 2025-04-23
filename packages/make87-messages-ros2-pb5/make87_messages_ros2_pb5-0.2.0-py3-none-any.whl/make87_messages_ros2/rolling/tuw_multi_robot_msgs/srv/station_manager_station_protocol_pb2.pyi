from make87_messages_ros2.rolling.tuw_multi_robot_msgs.msg import station_pb2 as _station_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StationManagerStationProtocolRequest(_message.Message):
    __slots__ = ("request", "station")
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    STATION_FIELD_NUMBER: _ClassVar[int]
    request: str
    station: _station_pb2.Station
    def __init__(self, request: _Optional[str] = ..., station: _Optional[_Union[_station_pb2.Station, _Mapping]] = ...) -> None: ...

class StationManagerStationProtocolResponse(_message.Message):
    __slots__ = ("response",)
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: str
    def __init__(self, response: _Optional[str] = ...) -> None: ...
