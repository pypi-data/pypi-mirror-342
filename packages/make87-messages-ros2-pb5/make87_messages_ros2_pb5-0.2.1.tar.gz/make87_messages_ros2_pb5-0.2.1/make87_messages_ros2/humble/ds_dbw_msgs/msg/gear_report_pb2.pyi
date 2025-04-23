from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.ds_dbw_msgs.msg import cmd_src_pb2 as _cmd_src_pb2
from make87_messages_ros2.humble.ds_dbw_msgs.msg import gear_pb2 as _gear_pb2
from make87_messages_ros2.humble.ds_dbw_msgs.msg import gear_reject_pb2 as _gear_reject_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GearReport(_message.Message):
    __slots__ = ("header", "ros2_header", "gear", "cmd", "driver", "reject", "power_latched", "external_control", "ready", "override_active", "override_other", "fault", "bad_crc", "degraded", "cmd_src")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    GEAR_FIELD_NUMBER: _ClassVar[int]
    CMD_FIELD_NUMBER: _ClassVar[int]
    DRIVER_FIELD_NUMBER: _ClassVar[int]
    REJECT_FIELD_NUMBER: _ClassVar[int]
    POWER_LATCHED_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_CONTROL_FIELD_NUMBER: _ClassVar[int]
    READY_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_OTHER_FIELD_NUMBER: _ClassVar[int]
    FAULT_FIELD_NUMBER: _ClassVar[int]
    BAD_CRC_FIELD_NUMBER: _ClassVar[int]
    DEGRADED_FIELD_NUMBER: _ClassVar[int]
    CMD_SRC_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    gear: _gear_pb2.Gear
    cmd: _gear_pb2.Gear
    driver: _gear_pb2.Gear
    reject: _gear_reject_pb2.GearReject
    power_latched: bool
    external_control: bool
    ready: bool
    override_active: bool
    override_other: bool
    fault: bool
    bad_crc: bool
    degraded: bool
    cmd_src: _cmd_src_pb2.CmdSrc
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., gear: _Optional[_Union[_gear_pb2.Gear, _Mapping]] = ..., cmd: _Optional[_Union[_gear_pb2.Gear, _Mapping]] = ..., driver: _Optional[_Union[_gear_pb2.Gear, _Mapping]] = ..., reject: _Optional[_Union[_gear_reject_pb2.GearReject, _Mapping]] = ..., power_latched: bool = ..., external_control: bool = ..., ready: bool = ..., override_active: bool = ..., override_other: bool = ..., fault: bool = ..., bad_crc: bool = ..., degraded: bool = ..., cmd_src: _Optional[_Union[_cmd_src_pb2.CmdSrc, _Mapping]] = ...) -> None: ...
