from make87_messages_ros2.jazzy.moveit_msgs.msg import motion_plan_request_pb2 as _motion_plan_request_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MotionSequenceItem(_message.Message):
    __slots__ = ("req", "blend_radius")
    REQ_FIELD_NUMBER: _ClassVar[int]
    BLEND_RADIUS_FIELD_NUMBER: _ClassVar[int]
    req: _motion_plan_request_pb2.MotionPlanRequest
    blend_radius: float
    def __init__(self, req: _Optional[_Union[_motion_plan_request_pb2.MotionPlanRequest, _Mapping]] = ..., blend_radius: _Optional[float] = ...) -> None: ...
