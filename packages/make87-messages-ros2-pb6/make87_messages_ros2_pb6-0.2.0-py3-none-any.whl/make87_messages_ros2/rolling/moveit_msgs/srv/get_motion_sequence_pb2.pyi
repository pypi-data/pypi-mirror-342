from make87_messages_ros2.rolling.moveit_msgs.msg import motion_sequence_request_pb2 as _motion_sequence_request_pb2
from make87_messages_ros2.rolling.moveit_msgs.msg import motion_sequence_response_pb2 as _motion_sequence_response_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetMotionSequenceRequest(_message.Message):
    __slots__ = ("request",)
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    request: _motion_sequence_request_pb2.MotionSequenceRequest
    def __init__(self, request: _Optional[_Union[_motion_sequence_request_pb2.MotionSequenceRequest, _Mapping]] = ...) -> None: ...

class GetMotionSequenceResponse(_message.Message):
    __slots__ = ("response",)
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: _motion_sequence_response_pb2.MotionSequenceResponse
    def __init__(self, response: _Optional[_Union[_motion_sequence_response_pb2.MotionSequenceResponse, _Mapping]] = ...) -> None: ...
