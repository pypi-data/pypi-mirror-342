from make87_messages_ros2.rolling.moveit_msgs.msg import planner_interface_description_pb2 as _planner_interface_description_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class QueryPlannerInterfacesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class QueryPlannerInterfacesResponse(_message.Message):
    __slots__ = ("planner_interfaces",)
    PLANNER_INTERFACES_FIELD_NUMBER: _ClassVar[int]
    planner_interfaces: _containers.RepeatedCompositeFieldContainer[_planner_interface_description_pb2.PlannerInterfaceDescription]
    def __init__(self, planner_interfaces: _Optional[_Iterable[_Union[_planner_interface_description_pb2.PlannerInterfaceDescription, _Mapping]]] = ...) -> None: ...
