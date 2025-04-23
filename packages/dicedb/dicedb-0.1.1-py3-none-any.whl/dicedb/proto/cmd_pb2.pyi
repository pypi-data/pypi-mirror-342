from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Command(_message.Message):
    __slots__ = ["args", "cmd"]
    ARGS_FIELD_NUMBER: ClassVar[int]
    CMD_FIELD_NUMBER: ClassVar[int]
    args: _containers.RepeatedScalarFieldContainer[str]
    cmd: str
    def __init__(self, cmd: Optional[str] = ..., args: Optional[Iterable[str]] = ...) -> None: ...
