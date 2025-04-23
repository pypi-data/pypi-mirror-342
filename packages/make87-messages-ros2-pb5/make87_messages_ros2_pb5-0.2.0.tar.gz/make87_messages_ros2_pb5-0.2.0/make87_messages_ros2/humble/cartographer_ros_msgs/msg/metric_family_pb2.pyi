from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.cartographer_ros_msgs.msg import metric_pb2 as _metric_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MetricFamily(_message.Message):
    __slots__ = ("header", "name", "description", "metrics")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    name: str
    description: str
    metrics: _containers.RepeatedCompositeFieldContainer[_metric_pb2.Metric]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., metrics: _Optional[_Iterable[_Union[_metric_pb2.Metric, _Mapping]]] = ...) -> None: ...
