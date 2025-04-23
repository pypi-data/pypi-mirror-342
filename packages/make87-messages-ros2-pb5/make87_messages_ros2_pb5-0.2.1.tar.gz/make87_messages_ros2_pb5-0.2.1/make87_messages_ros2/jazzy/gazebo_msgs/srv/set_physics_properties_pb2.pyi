from make87_messages_ros2.jazzy.gazebo_msgs.msg import ode_physics_pb2 as _ode_physics_pb2
from make87_messages_ros2.jazzy.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetPhysicsPropertiesRequest(_message.Message):
    __slots__ = ("time_step", "max_update_rate", "gravity", "ode_config")
    TIME_STEP_FIELD_NUMBER: _ClassVar[int]
    MAX_UPDATE_RATE_FIELD_NUMBER: _ClassVar[int]
    GRAVITY_FIELD_NUMBER: _ClassVar[int]
    ODE_CONFIG_FIELD_NUMBER: _ClassVar[int]
    time_step: float
    max_update_rate: float
    gravity: _vector3_pb2.Vector3
    ode_config: _ode_physics_pb2.ODEPhysics
    def __init__(self, time_step: _Optional[float] = ..., max_update_rate: _Optional[float] = ..., gravity: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., ode_config: _Optional[_Union[_ode_physics_pb2.ODEPhysics, _Mapping]] = ...) -> None: ...

class SetPhysicsPropertiesResponse(_message.Message):
    __slots__ = ("success", "status_message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    status_message: str
    def __init__(self, success: bool = ..., status_message: _Optional[str] = ...) -> None: ...
