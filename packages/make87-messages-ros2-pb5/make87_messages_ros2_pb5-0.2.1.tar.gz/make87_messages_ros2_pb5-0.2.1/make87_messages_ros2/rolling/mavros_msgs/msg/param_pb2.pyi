from make87_messages_ros2.rolling.mavros_msgs.msg import param_value_pb2 as _param_value_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Param(_message.Message):
    __slots__ = ("header", "param_id", "value", "param_index", "param_count")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PARAM_ID_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    PARAM_INDEX_FIELD_NUMBER: _ClassVar[int]
    PARAM_COUNT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    param_id: str
    value: _param_value_pb2.ParamValue
    param_index: int
    param_count: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., param_id: _Optional[str] = ..., value: _Optional[_Union[_param_value_pb2.ParamValue, _Mapping]] = ..., param_index: _Optional[int] = ..., param_count: _Optional[int] = ...) -> None: ...
