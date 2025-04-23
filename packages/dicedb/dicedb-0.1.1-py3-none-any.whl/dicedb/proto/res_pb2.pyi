from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor
ERR: Status
OK: Status

class DECRBYRes(_message.Message):
    __slots__ = ["value"]
    VALUE_FIELD_NUMBER: ClassVar[int]
    value: int
    def __init__(self, value: Optional[int] = ...) -> None: ...

class DECRRes(_message.Message):
    __slots__ = ["value"]
    VALUE_FIELD_NUMBER: ClassVar[int]
    value: int
    def __init__(self, value: Optional[int] = ...) -> None: ...

class DELRes(_message.Message):
    __slots__ = ["count"]
    COUNT_FIELD_NUMBER: ClassVar[int]
    count: int
    def __init__(self, count: Optional[int] = ...) -> None: ...

class ECHORes(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: ClassVar[int]
    message: str
    def __init__(self, message: Optional[str] = ...) -> None: ...

class EXISTSRes(_message.Message):
    __slots__ = ["count"]
    COUNT_FIELD_NUMBER: ClassVar[int]
    count: int
    def __init__(self, count: Optional[int] = ...) -> None: ...

class EXPIREATRes(_message.Message):
    __slots__ = ["is_changed"]
    IS_CHANGED_FIELD_NUMBER: ClassVar[int]
    is_changed: bool
    def __init__(self, is_changed: bool = ...) -> None: ...

class EXPIRERes(_message.Message):
    __slots__ = ["is_changed"]
    IS_CHANGED_FIELD_NUMBER: ClassVar[int]
    is_changed: bool
    def __init__(self, is_changed: bool = ...) -> None: ...

class EXPIRETIMERes(_message.Message):
    __slots__ = ["unix_sec"]
    UNIX_SEC_FIELD_NUMBER: ClassVar[int]
    unix_sec: int
    def __init__(self, unix_sec: Optional[int] = ...) -> None: ...

class FLUSHDBRes(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GETDELRes(_message.Message):
    __slots__ = ["value"]
    VALUE_FIELD_NUMBER: ClassVar[int]
    value: str
    def __init__(self, value: Optional[str] = ...) -> None: ...

class GETEXRes(_message.Message):
    __slots__ = ["value"]
    VALUE_FIELD_NUMBER: ClassVar[int]
    value: str
    def __init__(self, value: Optional[str] = ...) -> None: ...

class GETRes(_message.Message):
    __slots__ = ["value"]
    VALUE_FIELD_NUMBER: ClassVar[int]
    value: str
    def __init__(self, value: Optional[str] = ...) -> None: ...

class GETSETRes(_message.Message):
    __slots__ = ["value"]
    VALUE_FIELD_NUMBER: ClassVar[int]
    value: str
    def __init__(self, value: Optional[str] = ...) -> None: ...

class GETWATCHRes(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class HANDSHAKERes(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class HElement(_message.Message):
    __slots__ = ["key", "value"]
    KEY_FIELD_NUMBER: ClassVar[int]
    VALUE_FIELD_NUMBER: ClassVar[int]
    key: str
    value: str
    def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...

class HGETALLRes(_message.Message):
    __slots__ = ["elements"]
    ELEMENTS_FIELD_NUMBER: ClassVar[int]
    elements: _containers.RepeatedCompositeFieldContainer[HElement]
    def __init__(self, elements: Optional[Iterable[Union[HElement, Mapping]]] = ...) -> None: ...

class HGETALLWATCHRes(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class HGETRes(_message.Message):
    __slots__ = ["value"]
    VALUE_FIELD_NUMBER: ClassVar[int]
    value: str
    def __init__(self, value: Optional[str] = ...) -> None: ...

class HGETWATCHRes(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class HSETRes(_message.Message):
    __slots__ = ["count"]
    COUNT_FIELD_NUMBER: ClassVar[int]
    count: int
    def __init__(self, count: Optional[int] = ...) -> None: ...

class INCRBYRes(_message.Message):
    __slots__ = ["value"]
    VALUE_FIELD_NUMBER: ClassVar[int]
    value: int
    def __init__(self, value: Optional[int] = ...) -> None: ...

class INCRRes(_message.Message):
    __slots__ = ["value"]
    VALUE_FIELD_NUMBER: ClassVar[int]
    value: int
    def __init__(self, value: Optional[int] = ...) -> None: ...

class KEYSRes(_message.Message):
    __slots__ = ["keys"]
    KEYS_FIELD_NUMBER: ClassVar[int]
    keys: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, keys: Optional[Iterable[str]] = ...) -> None: ...

class PINGRes(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: ClassVar[int]
    message: str
    def __init__(self, message: Optional[str] = ...) -> None: ...

class Result(_message.Message):
    __slots__ = ["DECRBYRes", "DECRRes", "DELRes", "ECHORes", "EXISTSRes", "EXPIREATRes", "EXPIRERes", "EXPIRETIMERes", "FLUSHDBRes", "GETDELRes", "GETEXRes", "GETRes", "GETSETRes", "GETWATCHRes", "HANDSHAKERes", "HGETALLRes", "HGETALLWATCHRes", "HGETRes", "HGETWATCHRes", "HSETRes", "INCRBYRes", "INCRRes", "KEYSRes", "PINGRes", "SETRes", "TTLRes", "TYPERes", "UNWATCHRes", "ZADDRes", "ZCARDRes", "ZCARDWATCHRes", "ZCOUNTRes", "ZCOUNTWATCHRes", "ZPOPMAXRes", "ZPOPMINRes", "ZRANGERes", "ZRANGEWATCHRes", "ZRANKRes", "ZRANKWATCHRes", "ZREMRes", "fingerprint64", "message", "status"]
    DECRBYRES_FIELD_NUMBER: ClassVar[int]
    DECRBYRes: DECRBYRes
    DECRRES_FIELD_NUMBER: ClassVar[int]
    DECRRes: DECRRes
    DELRES_FIELD_NUMBER: ClassVar[int]
    DELRes: DELRes
    ECHORES_FIELD_NUMBER: ClassVar[int]
    ECHORes: ECHORes
    EXISTSRES_FIELD_NUMBER: ClassVar[int]
    EXISTSRes: EXISTSRes
    EXPIREATRES_FIELD_NUMBER: ClassVar[int]
    EXPIREATRes: EXPIREATRes
    EXPIRERES_FIELD_NUMBER: ClassVar[int]
    EXPIRERes: EXPIRERes
    EXPIRETIMERES_FIELD_NUMBER: ClassVar[int]
    EXPIRETIMERes: EXPIRETIMERes
    FINGERPRINT64_FIELD_NUMBER: ClassVar[int]
    FLUSHDBRES_FIELD_NUMBER: ClassVar[int]
    FLUSHDBRes: FLUSHDBRes
    GETDELRES_FIELD_NUMBER: ClassVar[int]
    GETDELRes: GETDELRes
    GETEXRES_FIELD_NUMBER: ClassVar[int]
    GETEXRes: GETEXRes
    GETRES_FIELD_NUMBER: ClassVar[int]
    GETRes: GETRes
    GETSETRES_FIELD_NUMBER: ClassVar[int]
    GETSETRes: GETSETRes
    GETWATCHRES_FIELD_NUMBER: ClassVar[int]
    GETWATCHRes: GETWATCHRes
    HANDSHAKERES_FIELD_NUMBER: ClassVar[int]
    HANDSHAKERes: HANDSHAKERes
    HGETALLRES_FIELD_NUMBER: ClassVar[int]
    HGETALLRes: HGETALLRes
    HGETALLWATCHRES_FIELD_NUMBER: ClassVar[int]
    HGETALLWATCHRes: HGETALLWATCHRes
    HGETRES_FIELD_NUMBER: ClassVar[int]
    HGETRes: HGETRes
    HGETWATCHRES_FIELD_NUMBER: ClassVar[int]
    HGETWATCHRes: HGETWATCHRes
    HSETRES_FIELD_NUMBER: ClassVar[int]
    HSETRes: HSETRes
    INCRBYRES_FIELD_NUMBER: ClassVar[int]
    INCRBYRes: INCRBYRes
    INCRRES_FIELD_NUMBER: ClassVar[int]
    INCRRes: INCRRes
    KEYSRES_FIELD_NUMBER: ClassVar[int]
    KEYSRes: KEYSRes
    MESSAGE_FIELD_NUMBER: ClassVar[int]
    PINGRES_FIELD_NUMBER: ClassVar[int]
    PINGRes: PINGRes
    SETRES_FIELD_NUMBER: ClassVar[int]
    SETRes: SETRes
    STATUS_FIELD_NUMBER: ClassVar[int]
    TTLRES_FIELD_NUMBER: ClassVar[int]
    TTLRes: TTLRes
    TYPERES_FIELD_NUMBER: ClassVar[int]
    TYPERes: TYPERes
    UNWATCHRES_FIELD_NUMBER: ClassVar[int]
    UNWATCHRes: UNWATCHRes
    ZADDRES_FIELD_NUMBER: ClassVar[int]
    ZADDRes: ZADDRes
    ZCARDRES_FIELD_NUMBER: ClassVar[int]
    ZCARDRes: ZCARDRes
    ZCARDWATCHRES_FIELD_NUMBER: ClassVar[int]
    ZCARDWATCHRes: ZCARDWATCHRes
    ZCOUNTRES_FIELD_NUMBER: ClassVar[int]
    ZCOUNTRes: ZCOUNTRes
    ZCOUNTWATCHRES_FIELD_NUMBER: ClassVar[int]
    ZCOUNTWATCHRes: ZCOUNTWATCHRes
    ZPOPMAXRES_FIELD_NUMBER: ClassVar[int]
    ZPOPMAXRes: ZPOPMAXRes
    ZPOPMINRES_FIELD_NUMBER: ClassVar[int]
    ZPOPMINRes: ZPOPMINRes
    ZRANGERES_FIELD_NUMBER: ClassVar[int]
    ZRANGERes: ZRANGERes
    ZRANGEWATCHRES_FIELD_NUMBER: ClassVar[int]
    ZRANGEWATCHRes: ZRANGEWATCHRes
    ZRANKRES_FIELD_NUMBER: ClassVar[int]
    ZRANKRes: ZRANKRes
    ZRANKWATCHRES_FIELD_NUMBER: ClassVar[int]
    ZRANKWATCHRes: ZRANKWATCHRes
    ZREMRES_FIELD_NUMBER: ClassVar[int]
    ZREMRes: ZREMRes
    fingerprint64: int
    message: str
    status: Status
    def __init__(self, status: Optional[Union[Status, str]] = ..., message: Optional[str] = ..., fingerprint64: Optional[int] = ..., TYPERes: Optional[Union[TYPERes, Mapping]] = ..., PINGRes: Optional[Union[PINGRes, Mapping]] = ..., ECHORes: Optional[Union[ECHORes, Mapping]] = ..., HANDSHAKERes: Optional[Union[HANDSHAKERes, Mapping]] = ..., EXISTSRes: Optional[Union[EXISTSRes, Mapping]] = ..., GETRes: Optional[Union[GETRes, Mapping]] = ..., SETRes: Optional[Union[SETRes, Mapping]] = ..., DELRes: Optional[Union[DELRes, Mapping]] = ..., KEYSRes: Optional[Union[KEYSRes, Mapping]] = ..., GETDELRes: Optional[Union[GETDELRes, Mapping]] = ..., GETEXRes: Optional[Union[GETEXRes, Mapping]] = ..., GETSETRes: Optional[Union[GETSETRes, Mapping]] = ..., INCRRes: Optional[Union[INCRRes, Mapping]] = ..., DECRRes: Optional[Union[DECRRes, Mapping]] = ..., INCRBYRes: Optional[Union[INCRBYRes, Mapping]] = ..., DECRBYRes: Optional[Union[DECRBYRes, Mapping]] = ..., FLUSHDBRes: Optional[Union[FLUSHDBRes, Mapping]] = ..., EXPIRERes: Optional[Union[EXPIRERes, Mapping]] = ..., EXPIREATRes: Optional[Union[EXPIREATRes, Mapping]] = ..., EXPIRETIMERes: Optional[Union[EXPIRETIMERes, Mapping]] = ..., TTLRes: Optional[Union[TTLRes, Mapping]] = ..., GETWATCHRes: Optional[Union[GETWATCHRes, Mapping]] = ..., UNWATCHRes: Optional[Union[UNWATCHRes, Mapping]] = ..., HGETRes: Optional[Union[HGETRes, Mapping]] = ..., HSETRes: Optional[Union[HSETRes, Mapping]] = ..., HGETALLRes: Optional[Union[HGETALLRes, Mapping]] = ..., HGETWATCHRes: Optional[Union[HGETWATCHRes, Mapping]] = ..., HGETALLWATCHRes: Optional[Union[HGETALLWATCHRes, Mapping]] = ..., ZADDRes: Optional[Union[ZADDRes, Mapping]] = ..., ZCOUNTRes: Optional[Union[ZCOUNTRes, Mapping]] = ..., ZRANGERes: Optional[Union[ZRANGERes, Mapping]] = ..., ZPOPMAXRes: Optional[Union[ZPOPMAXRes, Mapping]] = ..., ZREMRes: Optional[Union[ZREMRes, Mapping]] = ..., ZPOPMINRes: Optional[Union[ZPOPMINRes, Mapping]] = ..., ZRANKRes: Optional[Union[ZRANKRes, Mapping]] = ..., ZCARDRes: Optional[Union[ZCARDRes, Mapping]] = ..., ZRANGEWATCHRes: Optional[Union[ZRANGEWATCHRes, Mapping]] = ..., ZCOUNTWATCHRes: Optional[Union[ZCOUNTWATCHRes, Mapping]] = ..., ZCARDWATCHRes: Optional[Union[ZCARDWATCHRes, Mapping]] = ..., ZRANKWATCHRes: Optional[Union[ZRANKWATCHRes, Mapping]] = ...) -> None: ...

class SETRes(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class TTLRes(_message.Message):
    __slots__ = ["seconds"]
    SECONDS_FIELD_NUMBER: ClassVar[int]
    seconds: int
    def __init__(self, seconds: Optional[int] = ...) -> None: ...

class TYPERes(_message.Message):
    __slots__ = ["type"]
    TYPE_FIELD_NUMBER: ClassVar[int]
    type: str
    def __init__(self, type: Optional[str] = ...) -> None: ...

class UNWATCHRes(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ZADDRes(_message.Message):
    __slots__ = ["count"]
    COUNT_FIELD_NUMBER: ClassVar[int]
    count: int
    def __init__(self, count: Optional[int] = ...) -> None: ...

class ZCARDRes(_message.Message):
    __slots__ = ["count"]
    COUNT_FIELD_NUMBER: ClassVar[int]
    count: int
    def __init__(self, count: Optional[int] = ...) -> None: ...

class ZCARDWATCHRes(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ZCOUNTRes(_message.Message):
    __slots__ = ["count"]
    COUNT_FIELD_NUMBER: ClassVar[int]
    count: int
    def __init__(self, count: Optional[int] = ...) -> None: ...

class ZCOUNTWATCHRes(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ZElement(_message.Message):
    __slots__ = ["member", "score"]
    MEMBER_FIELD_NUMBER: ClassVar[int]
    SCORE_FIELD_NUMBER: ClassVar[int]
    member: str
    score: int
    def __init__(self, score: Optional[int] = ..., member: Optional[str] = ...) -> None: ...

class ZPOPMAXRes(_message.Message):
    __slots__ = ["elements"]
    ELEMENTS_FIELD_NUMBER: ClassVar[int]
    elements: _containers.RepeatedCompositeFieldContainer[ZElement]
    def __init__(self, elements: Optional[Iterable[Union[ZElement, Mapping]]] = ...) -> None: ...

class ZPOPMINRes(_message.Message):
    __slots__ = ["elements"]
    ELEMENTS_FIELD_NUMBER: ClassVar[int]
    elements: _containers.RepeatedCompositeFieldContainer[ZElement]
    def __init__(self, elements: Optional[Iterable[Union[ZElement, Mapping]]] = ...) -> None: ...

class ZRANGERes(_message.Message):
    __slots__ = ["elements"]
    ELEMENTS_FIELD_NUMBER: ClassVar[int]
    elements: _containers.RepeatedCompositeFieldContainer[ZElement]
    def __init__(self, elements: Optional[Iterable[Union[ZElement, Mapping]]] = ...) -> None: ...

class ZRANGEWATCHRes(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ZRANKRes(_message.Message):
    __slots__ = ["element", "rank"]
    ELEMENT_FIELD_NUMBER: ClassVar[int]
    RANK_FIELD_NUMBER: ClassVar[int]
    element: ZElement
    rank: int
    def __init__(self, rank: Optional[int] = ..., element: Optional[Union[ZElement, Mapping]] = ...) -> None: ...

class ZRANKWATCHRes(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ZREMRes(_message.Message):
    __slots__ = ["count"]
    COUNT_FIELD_NUMBER: ClassVar[int]
    count: int
    def __init__(self, count: Optional[int] = ...) -> None: ...

class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
