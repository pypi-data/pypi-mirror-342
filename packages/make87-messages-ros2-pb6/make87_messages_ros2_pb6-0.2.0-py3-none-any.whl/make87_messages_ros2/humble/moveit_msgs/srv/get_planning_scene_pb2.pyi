from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.moveit_msgs.msg import planning_scene_pb2 as _planning_scene_pb2
from make87_messages_ros2.humble.moveit_msgs.msg import planning_scene_components_pb2 as _planning_scene_components_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetPlanningSceneRequest(_message.Message):
    __slots__ = ("header", "components")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    COMPONENTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    components: _planning_scene_components_pb2.PlanningSceneComponents
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., components: _Optional[_Union[_planning_scene_components_pb2.PlanningSceneComponents, _Mapping]] = ...) -> None: ...

class GetPlanningSceneResponse(_message.Message):
    __slots__ = ("header", "scene")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SCENE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    scene: _planning_scene_pb2.PlanningScene
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., scene: _Optional[_Union[_planning_scene_pb2.PlanningScene, _Mapping]] = ...) -> None: ...
