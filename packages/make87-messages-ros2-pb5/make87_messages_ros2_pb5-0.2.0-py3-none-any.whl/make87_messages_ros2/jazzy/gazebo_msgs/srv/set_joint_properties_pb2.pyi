from make87_messages_ros2.jazzy.gazebo_msgs.msg import ode_joint_properties_pb2 as _ode_joint_properties_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetJointPropertiesRequest(_message.Message):
    __slots__ = ("joint_name", "ode_joint_config")
    JOINT_NAME_FIELD_NUMBER: _ClassVar[int]
    ODE_JOINT_CONFIG_FIELD_NUMBER: _ClassVar[int]
    joint_name: str
    ode_joint_config: _ode_joint_properties_pb2.ODEJointProperties
    def __init__(self, joint_name: _Optional[str] = ..., ode_joint_config: _Optional[_Union[_ode_joint_properties_pb2.ODEJointProperties, _Mapping]] = ...) -> None: ...

class SetJointPropertiesResponse(_message.Message):
    __slots__ = ("success", "status_message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    status_message: str
    def __init__(self, success: bool = ..., status_message: _Optional[str] = ...) -> None: ...
