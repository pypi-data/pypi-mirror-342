from make87_messages_ros2.jazzy.smacc2_msgs.msg import smacc_event_generator_pb2 as _smacc_event_generator_pb2
from make87_messages_ros2.jazzy.smacc2_msgs.msg import smacc_orthogonal_pb2 as _smacc_orthogonal_pb2
from make87_messages_ros2.jazzy.smacc2_msgs.msg import smacc_state_reactor_pb2 as _smacc_state_reactor_pb2
from make87_messages_ros2.jazzy.smacc2_msgs.msg import smacc_transition_pb2 as _smacc_transition_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SmaccState(_message.Message):
    __slots__ = ("index", "name", "children_states", "level", "transitions", "orthogonals", "state_reactors", "event_generators")
    INDEX_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CHILDREN_STATES_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    TRANSITIONS_FIELD_NUMBER: _ClassVar[int]
    ORTHOGONALS_FIELD_NUMBER: _ClassVar[int]
    STATE_REACTORS_FIELD_NUMBER: _ClassVar[int]
    EVENT_GENERATORS_FIELD_NUMBER: _ClassVar[int]
    index: int
    name: str
    children_states: _containers.RepeatedScalarFieldContainer[str]
    level: int
    transitions: _containers.RepeatedCompositeFieldContainer[_smacc_transition_pb2.SmaccTransition]
    orthogonals: _containers.RepeatedCompositeFieldContainer[_smacc_orthogonal_pb2.SmaccOrthogonal]
    state_reactors: _containers.RepeatedCompositeFieldContainer[_smacc_state_reactor_pb2.SmaccStateReactor]
    event_generators: _containers.RepeatedCompositeFieldContainer[_smacc_event_generator_pb2.SmaccEventGenerator]
    def __init__(self, index: _Optional[int] = ..., name: _Optional[str] = ..., children_states: _Optional[_Iterable[str]] = ..., level: _Optional[int] = ..., transitions: _Optional[_Iterable[_Union[_smacc_transition_pb2.SmaccTransition, _Mapping]]] = ..., orthogonals: _Optional[_Iterable[_Union[_smacc_orthogonal_pb2.SmaccOrthogonal, _Mapping]]] = ..., state_reactors: _Optional[_Iterable[_Union[_smacc_state_reactor_pb2.SmaccStateReactor, _Mapping]]] = ..., event_generators: _Optional[_Iterable[_Union[_smacc_event_generator_pb2.SmaccEventGenerator, _Mapping]]] = ...) -> None: ...
