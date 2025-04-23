"""Deserialize the server response into Python built-in types."""

from ..exceptions import DiceQueryError
from ..proto.res_pb2 import (
    ZADDRes,
    ZCOUNTRes,
    HSETRes,
    EXISTSRes,
    DELRes,
    ZREMRes,
    ZCARDRes,
    HGETRes,
    GETRes,
    GETEXRes,
    GETDELRes,
    INCRRes,
    DECRBYRes,
    INCRBYRes,
    GETSETRes,
    EXPIRERes,
    EXPIREATRes,
    EXPIRETIMERes,
    ZRANGERes,
    ZPOPMINRes,
    ZPOPMAXRes,
    PINGRes,
    ECHORes,
    DECRRes,
    Result,
    Status,
    TYPERes,
    HGETALLRes,
    TTLRes,
    KEYSRes,
    ZRANKRes,
)

from typing import Any, Union

_HAS_COUNT_FIELD = (
    ZADDRes,
    ZCOUNTRes,
    HSETRes,
    EXISTSRes,
    DELRes,
    ZREMRes,
    ZCARDRes,
)

_HAS_VALUE_FIELD = (
    HGETRes,
    GETRes,
    GETEXRes,
    GETDELRes,
    INCRRes,
    DECRRes,
    INCRBYRes,
    DECRBYRes,
    GETSETRes,
)

_HAS_IS_CHANGED_FIELD = (EXPIRERes, EXPIREATRes)

_HAS_Z_ELEMENTS_FIELD = (
    ZRANGERes,
    ZPOPMAXRes,
    ZPOPMINRes,
)

_HAS_MESSAGE_FIELD = (PINGRes, ECHORes)


def latest_value(raw_value: str, try_to_convert: bool) -> Union[int, str]:
    """Convert the raw value to the latest value.

    Args:
        raw_value (str): The raw value from the server.
        try_to_convert (bool): Whether to attempt conversion.

    Returns:
        Union[int, str]: The converted value, either as an int or str.
    """
    if try_to_convert:
        if isinstance(raw_value, str) and raw_value.isdigit():
            try:
                return int(raw_value)
            except ValueError:
                return raw_value
    return raw_value


def deserialize(result: Result, **kwargs) -> Any:
    """Deserialize the result from the server response into a Python object.

    Args:
        result (Result): The result object from the server.
        **kwargs: Additional keyword arguments for customization.

    Returns:
        Any: The deserialized Python object.
    """
    try_to_convert = kwargs.get('try_to_convert', False)
    if result.status == Status.ERR:
        raise DiceQueryError(result.message)

    if result.WhichOneof('response') is None:
        return None

    response = getattr(result, result.WhichOneof('response'))

    if isinstance(response, _HAS_COUNT_FIELD):
        return response.count

    if isinstance(response, _HAS_VALUE_FIELD):
        return latest_value(response.value, try_to_convert)

    if isinstance(response, _HAS_IS_CHANGED_FIELD):
        return response.is_changed

    if isinstance(response, _HAS_Z_ELEMENTS_FIELD):
        return {elm.member: elm.score for elm in response.elements}

    if isinstance(response, _HAS_MESSAGE_FIELD):
        return response.message

    if isinstance(response, TYPERes):
        return response.type

    if isinstance(response, HGETALLRes):
        res = {}
        for elm in response.elements:
            value = latest_value(elm.value, try_to_convert)
            res[elm.key] = value
        return res

    if isinstance(response, TTLRes):
        return response.seconds

    if isinstance(response, EXPIRETIMERes):
        return response.unix_sec

    if isinstance(response, KEYSRes):
        return list(response.keys)

    if isinstance(response, ZRANKRes):
        return response.rank

    return None