from make87_messages_ros2.jazzy.py_trees_ros_interfaces.msg import snapshot_stream_parameters_pb2 as _snapshot_stream_parameters_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OpenSnapshotStreamRequest(_message.Message):
    __slots__ = ("topic_name", "parameters")
    TOPIC_NAME_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    topic_name: str
    parameters: _snapshot_stream_parameters_pb2.SnapshotStreamParameters
    def __init__(self, topic_name: _Optional[str] = ..., parameters: _Optional[_Union[_snapshot_stream_parameters_pb2.SnapshotStreamParameters, _Mapping]] = ...) -> None: ...

class OpenSnapshotStreamResponse(_message.Message):
    __slots__ = ("topic_name",)
    TOPIC_NAME_FIELD_NUMBER: _ClassVar[int]
    topic_name: str
    def __init__(self, topic_name: _Optional[str] = ...) -> None: ...
