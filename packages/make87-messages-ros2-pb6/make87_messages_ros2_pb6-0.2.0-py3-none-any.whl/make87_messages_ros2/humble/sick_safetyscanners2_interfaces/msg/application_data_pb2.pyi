from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.sick_safetyscanners2_interfaces.msg import application_inputs_pb2 as _application_inputs_pb2
from make87_messages_ros2.humble.sick_safetyscanners2_interfaces.msg import application_outputs_pb2 as _application_outputs_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ApplicationData(_message.Message):
    __slots__ = ("header", "inputs", "outputs")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    INPUTS_FIELD_NUMBER: _ClassVar[int]
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    inputs: _application_inputs_pb2.ApplicationInputs
    outputs: _application_outputs_pb2.ApplicationOutputs
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., inputs: _Optional[_Union[_application_inputs_pb2.ApplicationInputs, _Mapping]] = ..., outputs: _Optional[_Union[_application_outputs_pb2.ApplicationOutputs, _Mapping]] = ...) -> None: ...
