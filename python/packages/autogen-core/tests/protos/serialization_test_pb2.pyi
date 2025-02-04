"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import google.protobuf.descriptor
import google.protobuf.message
import typing

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class ProtoMessage(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    MESSAGE_FIELD_NUMBER: builtins.int
    message: builtins.str
    def __init__(
        self,
        *,
        message: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["message", b"message"]) -> None: ...

global___ProtoMessage = ProtoMessage

@typing.final
class NestingProtoMessage(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    MESSAGE_FIELD_NUMBER: builtins.int
    NESTED_FIELD_NUMBER: builtins.int
    message: builtins.str
    @property
    def nested(self) -> global___ProtoMessage: ...
    def __init__(
        self,
        *,
        message: builtins.str = ...,
        nested: global___ProtoMessage | None = ...,
    ) -> None: ...
    def HasField(
        self, field_name: typing.Literal["nested", b"nested"]
    ) -> builtins.bool: ...
    def ClearField(
        self, field_name: typing.Literal["message", b"message", "nested", b"nested"]
    ) -> None: ...

global___NestingProtoMessage = NestingProtoMessage
