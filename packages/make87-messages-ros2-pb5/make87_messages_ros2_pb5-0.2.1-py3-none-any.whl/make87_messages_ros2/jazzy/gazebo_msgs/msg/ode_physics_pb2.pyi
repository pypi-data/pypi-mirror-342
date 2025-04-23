from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ODEPhysics(_message.Message):
    __slots__ = ("auto_disable_bodies", "sor_pgs_precon_iters", "sor_pgs_iters", "sor_pgs_w", "sor_pgs_rms_error_tol", "contact_surface_layer", "contact_max_correcting_vel", "cfm", "erp", "max_contacts")
    AUTO_DISABLE_BODIES_FIELD_NUMBER: _ClassVar[int]
    SOR_PGS_PRECON_ITERS_FIELD_NUMBER: _ClassVar[int]
    SOR_PGS_ITERS_FIELD_NUMBER: _ClassVar[int]
    SOR_PGS_W_FIELD_NUMBER: _ClassVar[int]
    SOR_PGS_RMS_ERROR_TOL_FIELD_NUMBER: _ClassVar[int]
    CONTACT_SURFACE_LAYER_FIELD_NUMBER: _ClassVar[int]
    CONTACT_MAX_CORRECTING_VEL_FIELD_NUMBER: _ClassVar[int]
    CFM_FIELD_NUMBER: _ClassVar[int]
    ERP_FIELD_NUMBER: _ClassVar[int]
    MAX_CONTACTS_FIELD_NUMBER: _ClassVar[int]
    auto_disable_bodies: bool
    sor_pgs_precon_iters: int
    sor_pgs_iters: int
    sor_pgs_w: float
    sor_pgs_rms_error_tol: float
    contact_surface_layer: float
    contact_max_correcting_vel: float
    cfm: float
    erp: float
    max_contacts: int
    def __init__(self, auto_disable_bodies: bool = ..., sor_pgs_precon_iters: _Optional[int] = ..., sor_pgs_iters: _Optional[int] = ..., sor_pgs_w: _Optional[float] = ..., sor_pgs_rms_error_tol: _Optional[float] = ..., contact_surface_layer: _Optional[float] = ..., contact_max_correcting_vel: _Optional[float] = ..., cfm: _Optional[float] = ..., erp: _Optional[float] = ..., max_contacts: _Optional[int] = ...) -> None: ...
