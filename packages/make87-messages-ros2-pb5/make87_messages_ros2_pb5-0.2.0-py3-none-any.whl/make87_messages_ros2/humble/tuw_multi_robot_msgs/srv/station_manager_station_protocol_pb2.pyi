from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.tuw_multi_robot_msgs.msg import station_pb2 as _station_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StationManagerStationProtocolRequest(_message.Message):
    __slots__ = ("header", "request", "station")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    STATION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    request: str
    station: _station_pb2.Station
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., request: _Optional[str] = ..., station: _Optional[_Union[_station_pb2.Station, _Mapping]] = ...) -> None: ...

class StationManagerStationProtocolResponse(_message.Message):
    __slots__ = ("header", "response")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    response: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., response: _Optional[str] = ...) -> None: ...
