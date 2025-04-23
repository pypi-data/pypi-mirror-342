from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.ds_dbw_msgs.msg import cmd_src_pb2 as _cmd_src_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ThrottleReport(_message.Message):
    __slots__ = ("header", "ros2_header", "cmd_type", "percent_input", "percent_cmd", "percent_output", "yield_request", "limiting_value", "limiting_rate", "external_control", "ready", "enabled", "override_active", "override_other", "override_latched", "timeout", "fault", "bad_crc", "bad_rc", "degraded", "limit_value", "cmd_src")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    CMD_TYPE_FIELD_NUMBER: _ClassVar[int]
    PERCENT_INPUT_FIELD_NUMBER: _ClassVar[int]
    PERCENT_CMD_FIELD_NUMBER: _ClassVar[int]
    PERCENT_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    YIELD_REQUEST_FIELD_NUMBER: _ClassVar[int]
    LIMITING_VALUE_FIELD_NUMBER: _ClassVar[int]
    LIMITING_RATE_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_CONTROL_FIELD_NUMBER: _ClassVar[int]
    READY_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_OTHER_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_LATCHED_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    FAULT_FIELD_NUMBER: _ClassVar[int]
    BAD_CRC_FIELD_NUMBER: _ClassVar[int]
    BAD_RC_FIELD_NUMBER: _ClassVar[int]
    DEGRADED_FIELD_NUMBER: _ClassVar[int]
    LIMIT_VALUE_FIELD_NUMBER: _ClassVar[int]
    CMD_SRC_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    cmd_type: int
    percent_input: float
    percent_cmd: float
    percent_output: float
    yield_request: bool
    limiting_value: bool
    limiting_rate: bool
    external_control: bool
    ready: bool
    enabled: bool
    override_active: bool
    override_other: bool
    override_latched: bool
    timeout: bool
    fault: bool
    bad_crc: bool
    bad_rc: bool
    degraded: bool
    limit_value: float
    cmd_src: _cmd_src_pb2.CmdSrc
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., cmd_type: _Optional[int] = ..., percent_input: _Optional[float] = ..., percent_cmd: _Optional[float] = ..., percent_output: _Optional[float] = ..., yield_request: bool = ..., limiting_value: bool = ..., limiting_rate: bool = ..., external_control: bool = ..., ready: bool = ..., enabled: bool = ..., override_active: bool = ..., override_other: bool = ..., override_latched: bool = ..., timeout: bool = ..., fault: bool = ..., bad_crc: bool = ..., bad_rc: bool = ..., degraded: bool = ..., limit_value: _Optional[float] = ..., cmd_src: _Optional[_Union[_cmd_src_pb2.CmdSrc, _Mapping]] = ...) -> None: ...
