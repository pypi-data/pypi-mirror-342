"""Custom exceptions for the DiceDB library."""

class DiceError(Exception):
    """Base class for all exceptions raised by the DiceDB library."""
    pass

class HandshakeFailedError(DiceError):
    """Exception raised when the handshake with the server fails."""
    pass

class DiceConnectionError(DiceError):
    """Exception raised for connection-related errors."""
    pass

class DiceSendCommandError(DiceConnectionError):
    """Exception raised when sending a command to the server fails."""
    pass

class DiceResponseTooLargeError(DiceError):
    """Exception raised when the response from the server is too large."""
    pass

class DiceCommandError(DiceError):
    """Exception raised for command-related errors."""
    pass

class DiceResponseError(DiceCommandError):
    """Exception raised for errors in the response from the server."""
    pass

class DiceParamError(DiceError):
    """Exception raised for parameter-related errors."""
    pass

class DiceQueryError(DiceError):
    """Exception raised for query-related errors."""
    pass

class DiceQueryEmptyResponseError(DiceQueryError):
    """Exception raised when a query returns an empty response."""
    pass