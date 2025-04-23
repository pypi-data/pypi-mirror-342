from make87_messages_ros2.rolling.std_msgs.msg import color_rgba_pb2 as _color_rgba_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class State(_message.Message):
    __slots__ = ("step", "list_node_open", "list_edge_open", "color_open", "list_node_closed", "list_edge_closed", "color_closed")
    STEP_FIELD_NUMBER: _ClassVar[int]
    LIST_NODE_OPEN_FIELD_NUMBER: _ClassVar[int]
    LIST_EDGE_OPEN_FIELD_NUMBER: _ClassVar[int]
    COLOR_OPEN_FIELD_NUMBER: _ClassVar[int]
    LIST_NODE_CLOSED_FIELD_NUMBER: _ClassVar[int]
    LIST_EDGE_CLOSED_FIELD_NUMBER: _ClassVar[int]
    COLOR_CLOSED_FIELD_NUMBER: _ClassVar[int]
    step: int
    list_node_open: _containers.RepeatedScalarFieldContainer[int]
    list_edge_open: _containers.RepeatedScalarFieldContainer[int]
    color_open: _containers.RepeatedCompositeFieldContainer[_color_rgba_pb2.ColorRGBA]
    list_node_closed: _containers.RepeatedScalarFieldContainer[int]
    list_edge_closed: _containers.RepeatedScalarFieldContainer[int]
    color_closed: _containers.RepeatedCompositeFieldContainer[_color_rgba_pb2.ColorRGBA]
    def __init__(self, step: _Optional[int] = ..., list_node_open: _Optional[_Iterable[int]] = ..., list_edge_open: _Optional[_Iterable[int]] = ..., color_open: _Optional[_Iterable[_Union[_color_rgba_pb2.ColorRGBA, _Mapping]]] = ..., list_node_closed: _Optional[_Iterable[int]] = ..., list_edge_closed: _Optional[_Iterable[int]] = ..., color_closed: _Optional[_Iterable[_Union[_color_rgba_pb2.ColorRGBA, _Mapping]]] = ...) -> None: ...
