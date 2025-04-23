from make87_messages_ros2.rolling.rmf_task_msgs.msg import alert_parameter_pb2 as _alert_parameter_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Alert(_message.Message):
    __slots__ = ("id", "title", "subtitle", "message", "display", "tier", "responses_available", "alert_parameters", "task_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    SUBTITLE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_FIELD_NUMBER: _ClassVar[int]
    TIER_FIELD_NUMBER: _ClassVar[int]
    RESPONSES_AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    ALERT_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    title: str
    subtitle: str
    message: str
    display: bool
    tier: int
    responses_available: _containers.RepeatedScalarFieldContainer[str]
    alert_parameters: _containers.RepeatedCompositeFieldContainer[_alert_parameter_pb2.AlertParameter]
    task_id: str
    def __init__(self, id: _Optional[str] = ..., title: _Optional[str] = ..., subtitle: _Optional[str] = ..., message: _Optional[str] = ..., display: bool = ..., tier: _Optional[int] = ..., responses_available: _Optional[_Iterable[str]] = ..., alert_parameters: _Optional[_Iterable[_Union[_alert_parameter_pb2.AlertParameter, _Mapping]]] = ..., task_id: _Optional[str] = ...) -> None: ...
