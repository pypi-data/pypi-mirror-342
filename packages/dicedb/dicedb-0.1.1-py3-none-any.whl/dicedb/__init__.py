"""DicDB Client Library."""

from .dice import Dice as Dice
from .exceptions import (
    HandshakeFailedError,
    DiceConnectionError,
    DiceSendCommandError,
    DiceResponseTooLargeError,
    DiceResponseError,
    DiceCommandError,
    DiceParamError,
)

__all__ = [
    "Dice",
    "HandshakeFailedError",
    "DiceConnectionError",
    "DiceSendCommandError",
    "DiceResponseTooLargeError",
    "DiceResponseError",
    "DiceCommandError",
    "DiceParamError",
]