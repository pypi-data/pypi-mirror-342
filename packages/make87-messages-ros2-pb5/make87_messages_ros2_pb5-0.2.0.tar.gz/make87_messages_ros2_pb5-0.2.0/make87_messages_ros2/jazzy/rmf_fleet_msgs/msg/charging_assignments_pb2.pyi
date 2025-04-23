from make87_messages_ros2.jazzy.rmf_fleet_msgs.msg import charging_assignment_pb2 as _charging_assignment_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ChargingAssignments(_message.Message):
    __slots__ = ("fleet_name", "assignments")
    FLEET_NAME_FIELD_NUMBER: _ClassVar[int]
    ASSIGNMENTS_FIELD_NUMBER: _ClassVar[int]
    fleet_name: str
    assignments: _containers.RepeatedCompositeFieldContainer[_charging_assignment_pb2.ChargingAssignment]
    def __init__(self, fleet_name: _Optional[str] = ..., assignments: _Optional[_Iterable[_Union[_charging_assignment_pb2.ChargingAssignment, _Mapping]]] = ...) -> None: ...
