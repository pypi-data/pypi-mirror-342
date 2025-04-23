from make87_messages_ros2.rolling.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.rolling.marti_nav_msgs.msg import route_pb2 as _route_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PlanRouteRequest(_message.Message):
    __slots__ = ("header", "waypoints", "plan_from_vehicle")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    WAYPOINTS_FIELD_NUMBER: _ClassVar[int]
    PLAN_FROM_VEHICLE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    waypoints: _containers.RepeatedCompositeFieldContainer[_pose_pb2.Pose]
    plan_from_vehicle: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., waypoints: _Optional[_Iterable[_Union[_pose_pb2.Pose, _Mapping]]] = ..., plan_from_vehicle: bool = ...) -> None: ...

class PlanRouteResponse(_message.Message):
    __slots__ = ("route", "success", "message", "cost")
    ROUTE_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    COST_FIELD_NUMBER: _ClassVar[int]
    route: _route_pb2.Route
    success: bool
    message: str
    cost: float
    def __init__(self, route: _Optional[_Union[_route_pb2.Route, _Mapping]] = ..., success: bool = ..., message: _Optional[str] = ..., cost: _Optional[float] = ...) -> None: ...
