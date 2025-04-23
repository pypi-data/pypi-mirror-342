from make87_messages_ros2.rolling.diagnostic_msgs.msg import diagnostic_status_pb2 as _diagnostic_status_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HazardStatus(_message.Message):
    __slots__ = ("level", "emergency", "emergency_holding", "diag_no_fault", "diag_safe_fault", "diag_latent_fault", "diag_single_point_fault")
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    EMERGENCY_FIELD_NUMBER: _ClassVar[int]
    EMERGENCY_HOLDING_FIELD_NUMBER: _ClassVar[int]
    DIAG_NO_FAULT_FIELD_NUMBER: _ClassVar[int]
    DIAG_SAFE_FAULT_FIELD_NUMBER: _ClassVar[int]
    DIAG_LATENT_FAULT_FIELD_NUMBER: _ClassVar[int]
    DIAG_SINGLE_POINT_FAULT_FIELD_NUMBER: _ClassVar[int]
    level: int
    emergency: bool
    emergency_holding: bool
    diag_no_fault: _containers.RepeatedCompositeFieldContainer[_diagnostic_status_pb2.DiagnosticStatus]
    diag_safe_fault: _containers.RepeatedCompositeFieldContainer[_diagnostic_status_pb2.DiagnosticStatus]
    diag_latent_fault: _containers.RepeatedCompositeFieldContainer[_diagnostic_status_pb2.DiagnosticStatus]
    diag_single_point_fault: _containers.RepeatedCompositeFieldContainer[_diagnostic_status_pb2.DiagnosticStatus]
    def __init__(self, level: _Optional[int] = ..., emergency: bool = ..., emergency_holding: bool = ..., diag_no_fault: _Optional[_Iterable[_Union[_diagnostic_status_pb2.DiagnosticStatus, _Mapping]]] = ..., diag_safe_fault: _Optional[_Iterable[_Union[_diagnostic_status_pb2.DiagnosticStatus, _Mapping]]] = ..., diag_latent_fault: _Optional[_Iterable[_Union[_diagnostic_status_pb2.DiagnosticStatus, _Mapping]]] = ..., diag_single_point_fault: _Optional[_Iterable[_Union[_diagnostic_status_pb2.DiagnosticStatus, _Mapping]]] = ...) -> None: ...
