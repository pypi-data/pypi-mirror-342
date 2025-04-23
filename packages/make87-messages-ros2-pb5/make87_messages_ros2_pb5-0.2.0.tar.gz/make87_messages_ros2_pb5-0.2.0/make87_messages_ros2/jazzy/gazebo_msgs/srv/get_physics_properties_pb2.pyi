from make87_messages_ros2.jazzy.gazebo_msgs.msg import ode_physics_pb2 as _ode_physics_pb2
from make87_messages_ros2.jazzy.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetPhysicsPropertiesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetPhysicsPropertiesResponse(_message.Message):
    __slots__ = ("time_step", "pause", "max_update_rate", "gravity", "ode_config", "success", "status_message")
    TIME_STEP_FIELD_NUMBER: _ClassVar[int]
    PAUSE_FIELD_NUMBER: _ClassVar[int]
    MAX_UPDATE_RATE_FIELD_NUMBER: _ClassVar[int]
    GRAVITY_FIELD_NUMBER: _ClassVar[int]
    ODE_CONFIG_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    time_step: float
    pause: bool
    max_update_rate: float
    gravity: _vector3_pb2.Vector3
    ode_config: _ode_physics_pb2.ODEPhysics
    success: bool
    status_message: str
    def __init__(self, time_step: _Optional[float] = ..., pause: bool = ..., max_update_rate: _Optional[float] = ..., gravity: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., ode_config: _Optional[_Union[_ode_physics_pb2.ODEPhysics, _Mapping]] = ..., success: bool = ..., status_message: _Optional[str] = ...) -> None: ...
