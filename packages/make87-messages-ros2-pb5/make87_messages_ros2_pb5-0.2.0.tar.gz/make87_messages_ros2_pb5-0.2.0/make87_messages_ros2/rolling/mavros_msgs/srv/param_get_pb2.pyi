from make87_messages_ros2.rolling.mavros_msgs.msg import param_value_pb2 as _param_value_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ParamGetRequest(_message.Message):
    __slots__ = ("param_id",)
    PARAM_ID_FIELD_NUMBER: _ClassVar[int]
    param_id: str
    def __init__(self, param_id: _Optional[str] = ...) -> None: ...

class ParamGetResponse(_message.Message):
    __slots__ = ("success", "value")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    value: _param_value_pb2.ParamValue
    def __init__(self, success: bool = ..., value: _Optional[_Union[_param_value_pb2.ParamValue, _Mapping]] = ...) -> None: ...
