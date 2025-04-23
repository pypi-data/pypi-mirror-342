from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.vimbax_camera_msgs.msg import error_pb2 as _error_pb2
from make87_messages_ros2.humble.vimbax_camera_msgs.msg import feature_module_pb2 as _feature_module_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FeatureFloatInfoGetRequest(_message.Message):
    __slots__ = ("header", "feature_name", "feature_module")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FEATURE_NAME_FIELD_NUMBER: _ClassVar[int]
    FEATURE_MODULE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    feature_name: str
    feature_module: _feature_module_pb2.FeatureModule
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., feature_name: _Optional[str] = ..., feature_module: _Optional[_Union[_feature_module_pb2.FeatureModule, _Mapping]] = ...) -> None: ...

class FeatureFloatInfoGetResponse(_message.Message):
    __slots__ = ("header", "min", "max", "inc", "inc_available", "error")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MIN_FIELD_NUMBER: _ClassVar[int]
    MAX_FIELD_NUMBER: _ClassVar[int]
    INC_FIELD_NUMBER: _ClassVar[int]
    INC_AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    min: float
    max: float
    inc: float
    inc_available: bool
    error: _error_pb2.Error
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., min: _Optional[float] = ..., max: _Optional[float] = ..., inc: _Optional[float] = ..., inc_available: bool = ..., error: _Optional[_Union[_error_pb2.Error, _Mapping]] = ...) -> None: ...
