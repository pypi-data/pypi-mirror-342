from make87_messages_ros2.jazzy.marti_nav_msgs.msg import route_pb2 as _route_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetRouteRequest(_message.Message):
    __slots__ = ("guid",)
    GUID_FIELD_NUMBER: _ClassVar[int]
    guid: str
    def __init__(self, guid: _Optional[str] = ...) -> None: ...

class GetRouteResponse(_message.Message):
    __slots__ = ("route", "success", "message")
    ROUTE_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    route: _route_pb2.Route
    success: bool
    message: str
    def __init__(self, route: _Optional[_Union[_route_pb2.Route, _Mapping]] = ..., success: bool = ..., message: _Optional[str] = ...) -> None: ...
