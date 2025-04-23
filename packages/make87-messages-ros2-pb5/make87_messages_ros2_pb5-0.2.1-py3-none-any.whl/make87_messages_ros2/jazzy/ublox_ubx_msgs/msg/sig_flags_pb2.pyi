from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SigFlags(_message.Message):
    __slots__ = ("health", "pr_smoothed", "pr_used", "cr_used", "do_used", "pr_corr_used", "cr_corr_used", "do_corr_used")
    HEALTH_FIELD_NUMBER: _ClassVar[int]
    PR_SMOOTHED_FIELD_NUMBER: _ClassVar[int]
    PR_USED_FIELD_NUMBER: _ClassVar[int]
    CR_USED_FIELD_NUMBER: _ClassVar[int]
    DO_USED_FIELD_NUMBER: _ClassVar[int]
    PR_CORR_USED_FIELD_NUMBER: _ClassVar[int]
    CR_CORR_USED_FIELD_NUMBER: _ClassVar[int]
    DO_CORR_USED_FIELD_NUMBER: _ClassVar[int]
    health: int
    pr_smoothed: bool
    pr_used: bool
    cr_used: bool
    do_used: bool
    pr_corr_used: bool
    cr_corr_used: bool
    do_corr_used: bool
    def __init__(self, health: _Optional[int] = ..., pr_smoothed: bool = ..., pr_used: bool = ..., cr_used: bool = ..., do_used: bool = ..., pr_corr_used: bool = ..., cr_corr_used: bool = ..., do_corr_used: bool = ...) -> None: ...
