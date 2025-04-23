from make87_messages_ros2.rolling.moveit_msgs.msg import constraint_eval_result_pb2 as _constraint_eval_result_pb2
from make87_messages_ros2.rolling.moveit_msgs.msg import constraints_pb2 as _constraints_pb2
from make87_messages_ros2.rolling.moveit_msgs.msg import contact_information_pb2 as _contact_information_pb2
from make87_messages_ros2.rolling.moveit_msgs.msg import cost_source_pb2 as _cost_source_pb2
from make87_messages_ros2.rolling.moveit_msgs.msg import robot_state_pb2 as _robot_state_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetStateValidityRequest(_message.Message):
    __slots__ = ("robot_state", "group_name", "constraints")
    ROBOT_STATE_FIELD_NUMBER: _ClassVar[int]
    GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    CONSTRAINTS_FIELD_NUMBER: _ClassVar[int]
    robot_state: _robot_state_pb2.RobotState
    group_name: str
    constraints: _constraints_pb2.Constraints
    def __init__(self, robot_state: _Optional[_Union[_robot_state_pb2.RobotState, _Mapping]] = ..., group_name: _Optional[str] = ..., constraints: _Optional[_Union[_constraints_pb2.Constraints, _Mapping]] = ...) -> None: ...

class GetStateValidityResponse(_message.Message):
    __slots__ = ("valid", "contacts", "cost_sources", "constraint_result")
    VALID_FIELD_NUMBER: _ClassVar[int]
    CONTACTS_FIELD_NUMBER: _ClassVar[int]
    COST_SOURCES_FIELD_NUMBER: _ClassVar[int]
    CONSTRAINT_RESULT_FIELD_NUMBER: _ClassVar[int]
    valid: bool
    contacts: _containers.RepeatedCompositeFieldContainer[_contact_information_pb2.ContactInformation]
    cost_sources: _containers.RepeatedCompositeFieldContainer[_cost_source_pb2.CostSource]
    constraint_result: _containers.RepeatedCompositeFieldContainer[_constraint_eval_result_pb2.ConstraintEvalResult]
    def __init__(self, valid: bool = ..., contacts: _Optional[_Iterable[_Union[_contact_information_pb2.ContactInformation, _Mapping]]] = ..., cost_sources: _Optional[_Iterable[_Union[_cost_source_pb2.CostSource, _Mapping]]] = ..., constraint_result: _Optional[_Iterable[_Union[_constraint_eval_result_pb2.ConstraintEvalResult, _Mapping]]] = ...) -> None: ...
