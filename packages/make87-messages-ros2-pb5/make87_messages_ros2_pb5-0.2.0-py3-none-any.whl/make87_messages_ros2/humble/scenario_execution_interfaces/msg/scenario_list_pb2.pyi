from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.scenario_execution_interfaces.msg import scenario_pb2 as _scenario_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ScenarioList(_message.Message):
    __slots__ = ("header", "scenarios")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SCENARIOS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    scenarios: _containers.RepeatedCompositeFieldContainer[_scenario_pb2.Scenario]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., scenarios: _Optional[_Iterable[_Union[_scenario_pb2.Scenario, _Mapping]]] = ...) -> None: ...
