from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class NewMqtt2RosBridgeRequest(_message.Message):
    __slots__ = ("ros_topic", "mqtt_topic", "primitive", "mqtt_qos", "ros_queue_size", "ros_latched")
    ROS_TOPIC_FIELD_NUMBER: _ClassVar[int]
    MQTT_TOPIC_FIELD_NUMBER: _ClassVar[int]
    PRIMITIVE_FIELD_NUMBER: _ClassVar[int]
    MQTT_QOS_FIELD_NUMBER: _ClassVar[int]
    ROS_QUEUE_SIZE_FIELD_NUMBER: _ClassVar[int]
    ROS_LATCHED_FIELD_NUMBER: _ClassVar[int]
    ros_topic: str
    mqtt_topic: str
    primitive: bool
    mqtt_qos: int
    ros_queue_size: int
    ros_latched: bool
    def __init__(self, ros_topic: _Optional[str] = ..., mqtt_topic: _Optional[str] = ..., primitive: bool = ..., mqtt_qos: _Optional[int] = ..., ros_queue_size: _Optional[int] = ..., ros_latched: bool = ...) -> None: ...

class NewMqtt2RosBridgeResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
